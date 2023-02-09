import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from UI.UI_login_window import Ui_widget
from UI.window_lang import LT
import os
import pandas as pd
import socket
import logging

logging.basicConfig(level=logging.INFO)


class LoginWindow(QWidget, Ui_widget):

    authenticated = pyqtSignal()
    LANGUAGE = "CN"
    host_server = ""
    port_server = 8888

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.initialize()
        # TODO:
        self.setStyleSheet("QTextBrowser:{background: palette(window);}")
        self.get_local()
        self.server_config()
        self.connect_slots()
        self.show()

    def initialize(self):
        self.setWindowTitle(f"{LT.window_title[self.LANGUAGE]}")
        self.checkBox.setChecked(False)
        self.lineEdit_hostname.setEnabled(True)
        self.lineEdit_ip.setEnabled(False)
        self.label_2.setText(f"{LT.username[self.LANGUAGE]}")
        self.label_3.setText(f"{LT.password[self.LANGUAGE]}")
        self.submit_button.setText(f"{LT.button_login[self.LANGUAGE]}")
        self.settings_button.setText(f"{LT.settings[self.LANGUAGE]}")
        self.settings_group.setTitle(f"{LT.settings[self.LANGUAGE]}")
        self.label_5.setText(f"{LT.ip[self.LANGUAGE]}")
        self.label_6.setText(f"{LT.port[self.LANGUAGE]}")
        self.settings_submit_button.setText(f"{LT.submit[self.LANGUAGE]}")
        self.settings_reset_button.setText(f"{LT.reset[self.LANGUAGE]}")

        # self.label_4.setPixmap(
        #     QPixmap(":/images/aurora_logo.png").scaled(
        #         QSize(258, 200), Qt.KeepAspectRatio, Qt.SmoothTransformation
        #     )
        # )

        self.legalese_label.setOpenExternalLinks(True)
        self.settings_button.setCheckable(True)
        self.settings_group.setVisible(False)
        self.submit_button.setEnabled(False)
        self.submit_button.setText(f"{LT.button_term[self.LANGUAGE]}")
        # self.setFixedSize(599, 409)
        self.initial_size = self.sizeHint()
        self.setFixedSize(self.initial_size)

        # Your code ends here

    def connect_slots(self):
        self.legalese_checkBox.stateChanged.connect(self.check_term)
        self.settings_button.toggled.connect(self.toggle_settings)
        self.settings_reset_button.clicked.connect(self.reset_settings)
        self.settings_submit_button.clicked.connect(self.submit_settings)
        self.checkBox.stateChanged.connect(self.munual_settings)

    @pyqtSlot(str)
    def set_button_text(self, text):
        if text:
            self.submit_button.setText(f"{LT.button_login[self.LANGUAGE]} {text}")
        else:
            self.submit_button.setText(f"{LT.button_login[self.LANGUAGE]}")

    @pyqtSlot()
    def check_term(self):
        if self.legalese_checkBox.isChecked() == True:
            self.submit_button.setEnabled(True)
            self.submit_button.setText(f"{LT.button_login[self.LANGUAGE]}")
        else:
            self.submit_button.setEnabled(False)
            self.submit_button.setText(f"{LT.button_term[self.LANGUAGE]}")

    def toggle_settings(self):
        if self.settings_button.isChecked() == True:
            self.settings_group.setVisible(True)
            self.enlarged_size = self.sizeHint()
            self.setFixedSize(self.enlarged_size)
        else:
            self.settings_group.setVisible(False)
            self.setFixedSize(self.initial_size)

    def reset_settings(self):
        self.checkBox.setChecked(False)
        self.lineEdit_hostname.setEnabled(True)
        self.lineEdit_ip.setEnabled(False)
        self.lineEdit_hostname.setText(self.host_server)
        self.lineEdit_ip.setText("")
        self.spinBox_port.setValue(int(self.port_server))

    def munual_settings(self):
        if self.checkBox.isChecked() == True:
            self.lineEdit_hostname.setEnabled(False)
            self.lineEdit_ip.setEnabled(True)
        else:
            self.lineEdit_ip.setEnabled(False)
            self.lineEdit_hostname.setEnabled(True)

    def submit_settings(self):
        self.server_config()
        server_ip_df = pd.DataFrame(
            data={
                "hostname": [self.lineEdit_hostname.text()],
                "ip": [self.lineEdit_ip.text()],
                "port": [self.spinBox_port.value()],
            }
        )
        server_ip_df.to_csv(r"temp/server_ip.csv", index=False, header=True)
        QMessageBox.information(self, "成功", "服务器地址及端口已保存")
        logging.info(self.server_ip)
        logging.info(self.server_port)

    def get_local(self):
        if os.path.exists(r"temp/server_ip.csv") == False:
            server_ip_df = pd.DataFrame(
                data={"hostname": [""], "ip": [""], "port": ["8888"]}
            )
        else:
            server_ip_df = pd.read_csv(
                r"temp/server_ip.csv",
                header=0,
                dtype={
                    "hostname": object,
                    "ip": object,
                    "port": int,
                },
            )
        if str(server_ip_df["hostname"][0])=='nan':
            self.checkBox.setChecked(True)
            self.lineEdit_hostname.setEnabled(False)
            self.lineEdit_ip.setEnabled(True)
            self.lineEdit_ip.setText(str(server_ip_df["ip"][0]))

        else:            
            self.checkBox.setChecked(False)
            self.lineEdit_hostname.setEnabled(True)
            self.lineEdit_ip.setEnabled(False)
            self.lineEdit_hostname.setText(str(server_ip_df["hostname"][0]))



        self.spinBox_port.setValue(int(server_ip_df["port"][0]))

    def server_config(self):
        if self.checkBox.isChecked() == False:
            try:
                self.server_ip = socket.gethostbyname(self.lineEdit_hostname.text())
            except Exception as e:
                self.server_ip = ""
                QMessageBox.critical(self, "Hostname错误", "请重新输入服务器信息")
            finally:
                self.lineEdit_ip.setText("")
        else:
            self.lineEdit_hostname.setText("")
            self.server_ip = self.lineEdit_ip.text()

        self.hostname = self.lineEdit_hostname.text()
        self.server_port = self.spinBox_port.value()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = LoginWindow()
    sys.exit(app.exec_())
