from retrying import retry
from .etrade_url import *
import requests
from rauth import OAuth1Service
import time
import logging

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


class ETradeAccSession(requests.Session):
    def __init__(self, username, password, consumer_key, consumer_secret):
        super().__init__()
        self.username = username
        self.password = password
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_oauth(self):
        """
           First get request_token
                     request_token_secret
           Second get authorize_url
        """
        ck = self.consumer_key
        cs = self.consumer_secret
        etrade = OAuth1Service(
            name="etrade",
            consumer_key=ck,
            consumer_secret=cs,
            request_token_url="https://api.etrade.com/oauth/request_token",
            access_token_url="https://api.etrade.com/oauth/access_token",
            authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
            base_url="https://api.etrade.com")

        request_token, request_token_secret = etrade.get_request_token(
            params={"oauth_callback": "oob", "format": "json"})
        authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
        return etrade, request_token, request_token_secret, authorize_url

    def get_oauth_verifier(self):
        """
           使用Chrome浏览器获取授权网页，并授权使用API
           获取 oauth_verifier
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--useAutomationExtension=false")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        a, b, c, d = self.get_oauth()
        driver.get(d)
        logging.info("opened link")
        user_name_present = EC.presence_of_element_located((By.ID, "user_orig"))
        WebDriverWait(driver, TIME_OUT).until(user_name_present)
        user_name_el = driver.find_element(By.ID, "user_orig")
        password_el = driver.find_element(By.NAME, "PASSWORD")
        user_name_el.send_keys(self.username)
        password_el.send_keys(self.password)
        swhcookie = {'name': 'SWH', 'value': 'ETWLCUST1-be5fbc48-91fb', 'domain': '.etrade.com', 'secure': True,
                     'httpOnly': True}
        driver.add_cookie(swhcookie)
        submit_form_el = driver.find_element(By.ID, "logon_button")
        submit_form_el.click()
        logging.info("click accept")
        accept_agreement = EC.element_to_be_clickable((By.CLASS_NAME, "api-inner-container"))
        WebDriverWait(driver, TIME_OUT).until(accept_agreement)
        accept_option = driver.find_element(By.XPATH, "//*[@value='Accept']")
        accept_option.click()
        verifier_web = EC.visibility_of_element_located((By.CLASS_NAME, "api-footer"))
        WebDriverWait(driver, TIME_OUT).until(verifier_web)
        oauth_verifier = driver.find_element(By.TAG_NAME, 'input').get_attribute('value')
        """
        判断返回值是否为空
        """
        if oauth_verifier is not None:
            logging.info(oauth_verifier)
            return oauth_verifier
        else:
            pass

    def get_session(self):
        """
        获取 session 获的登录基础
        """
        a, b, c, d = self.get_oauth()
        oauth_verifier = self.get_oauth_verifier()
        try:
            session = a.get_auth_session(b, c, params={"oauth_verifier": oauth_verifier})
            if session.verify is True:
                return session
            else:
                pass

        except Exception:
            return "Error", "验证失败"







if __name__ == "__main__":
    et = ETradeAccSession()
    et.get_oauth_verifier()
