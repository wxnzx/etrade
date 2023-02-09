from .ib_url import *
import pandas as pd
import json
import requests
import subprocess
import time
import logging
import socket
from selenium import webdriver
from selenium.common.exceptions import (
    WebDriverException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

formatter = "[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=formatter)


class IBAccSession(requests.Session):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password
        self._headers = {}
        self.session_refresh_time = None

    def _request(self, *args, **kwargs):
        self._reconnect()
        headers = {"User-Agent": "Console", "content-type": "application/json"}
        return super().request(*args, **kwargs, headers=headers, verify=False)

    def _reconnect(self):
        if not self._is_port_in_use():
            self._start_server()
        if not self._is_authenticated():
            self._authenticate_gateway()
        if self._is_validate_needed():
            self._keep_session_alive()

    def _authenticate_gateway(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--ignore-ssl-errors=yes")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--useAutomationExtension=false")
            options.add_argument("--disable-extensions")
            options.add_argument("--dns-prefetch-disable")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            driver.get("https://localhost:5000/sso/Login?forwardTo=22&RL=1&ip2loc=on")
            logging.info("opened link")
            user_name_present = EC.presence_of_element_located((By.ID, "user_name"))
            WebDriverWait(driver, TIME_OUT).until(user_name_present)
            user_name_el = driver.find_element(By.ID, "user_name")
            password_el = driver.find_element(By.ID, "password")
            user_name_el.send_keys(self.username)
            password_el.send_keys(self.password)
            time.sleep(TIME_OUT)
            submit_form_el = driver.find_element(By.ID, "submitForm")
            logging.info("submitted")
            submit_form_el.click()
            success_present = EC.text_to_be_present_in_element(
                (By.TAG_NAME, "pre"), "Client login succeeds"
            )
            two_factor_input_present = EC.visibility_of_element_located(
                (By.ID, "twofactbase")
            )
            error_displayed = EC.visibility_of_element_located((By.ID, "ERRORMSG"))
            ibkey_promo_skip_clickable = EC.element_to_be_clickable(
                (By.CLASS_NAME, "ibkey-promo-skip")
            )

            trigger = WebDriverWait(driver, TIME_OUT).until(
                EC.any_of(
                    success_present,
                    two_factor_input_present,
                    error_displayed,
                    ibkey_promo_skip_clickable,
                )
            )
            trigger_id = trigger.get_attribute("id")
            trigger_class = trigger.get_attribute("class")
            logging.info(trigger_id)
            logging.info(trigger_class)
            if trigger_class == "ibkey-promo-skip":
                logging.info("Handling IB-Key promo display...")
                trigger.click()
                WebDriverWait(driver, TIME_OUT).until(success_present)
            if trigger_id == "ERRORMSG":
                return False, trigger.text
            elif trigger.id == "twofactbase":
                return False, trigger.text
            else:
                return True, ""

        except TimeoutException as e:
            logging.info(str(e))
            return False, str(e)
        except Exception as e:
            logging.info(str(e))
            return False, str(e)

    def _keep_session_alive(self):
        VALIDATE = "sso/validate"
        resp = requests.post(BASE + VALIDATE, verify=False)
        self.session_refresh_time = time.time()

    def _is_validate_needed(self):
        if self.session_refresh_time == None:
            return True
        elif time.time() - self.session_refresh_time >= 60:
            return True
        else:
            return False

    def _is_port_in_use(self, port: int = 5000) -> bool:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def _start_server(self) -> str:
        """Starts the Server.
        Returns:
        ----
        str: The Server Process ID.
        """
        if not self._is_port_in_use():

            # path = pathlib.Path(__file__).parent.joinpath("clientportal.gw").resolve()
            # path = r"C:\Git\trading_software\temp\clientportal.gw"
            path = r"C:\git\trading_software\temp\clientportal.gw"
            logging.info(path)
            IB_WEB_API_PROC = ["cmd", "/k", r"bin\run.bat", r"root\conf.yaml"]
            self.server_process = subprocess.Popen(
                args=IB_WEB_API_PROC,
                cwd=path,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            ).pid
            logging.info(self.server_process)

    def _is_authenticated(self) -> bool:
        try:
            resp = requests.get(BASE + AUTHENTICATION, verify=False)
        except Exception:
            return False
        else:
            if resp.status_code != 200:
                return False

            elif resp.json()["authenticated"] == False:
                return False
            else:
                return True


if __name__ == "__main__":
    ib_session = IBAccSession()
    ib_session._reconnect()
