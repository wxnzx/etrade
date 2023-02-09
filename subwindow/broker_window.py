import sys
from PyQt5.QtWidgets import (
    QWidget,
    QTabBar,
    QMessageBox,
    QAbstractItemView,
    QApplication,
    QTableView,
)
from PyQt5.QtCore import pyqtSignal
import pandas as pd
import json
import os

from account import AuroraAccount, BrokerBase, FutuAcc, TDAcc, IBAcc, ETradeAcc
from utils.worker.get_acc_list_thread import AccListThread
from utils.worker.auth_thread import AuthThread
from UI.UI_broker_window import Ui_Form
from UI.data_model import pandasModel
from UI.window_lang import BT
import logging

logging.basicConfig(level=logging.INFO)


class BrokerWindow(QWidget, Ui_Form):

    authenticated = pyqtSignal(object)
    deleted = pyqtSignal(object)
    aurora_account = AuroraAccount()
    LANGUAGE = "CN"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initialize()
        self.move(1210, 70)
        # jimmy
        self.load_layout()
        self.connect_slots()
        self.show()

    def initialize(self):
        self.setWindowTitle(f"{BT.window_title[self.LANGUAGE]}")
        # self.label_6.setText(f"{BT.label_verify[self.LANGUAGE]}")
        # self.verify_button.setText(f"{BT.button_verify[self.LANGUAGE]}")
        # self.label_4.setText(f"{BT.label_verified_acc[self.LANGUAGE]}")
        # self.label_8.setText(f"{BT.label_delete[self.LANGUAGE]}")
        # self.delete_button.setText(f"{BT.button_delete[self.LANGUAGE]}")
        # self.label_7.setText(f"{BT.label_delete_all[self.LANGUAGE]}")
        # self.delete_local_button.setText(f"{BT.button_delete_all[self.LANGUAGE]}")
        self.label.setText(f"{BT.label_add[self.LANGUAGE]}")
        self.label_12.setText(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
            '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            f'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{BT.label_disclaimer[self.LANGUAGE][0]}</p>\n'
            f'<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{BT.label_disclaimer[self.LANGUAGE][1]}</p></body></html>'
        )
        self.pushButton_getAccList.setText(f"{BT.button_get_acc[self.LANGUAGE]}")
        self.label_11.setText(f"{BT.label_select_acc[self.LANGUAGE]}")
        self.label_5.setText(f"{BT.label_trading_pass[self.LANGUAGE]}")
        self.add_broker_button.setText(f"{BT.button_add[self.LANGUAGE]}")
        self.groupBox_add.setTitle(f"{BT.group_add[self.LANGUAGE]}")
        # self.groupBox_verify.setTitle(f"{BT.group_verify[self.LANGUAGE]}")
        self.groupBox_delete.setTitle(f"{BT.group_delete[self.LANGUAGE]}")

        self.pushButton_generateToken.setEnabled(False)
        self.add_broker_button.setEnabled(False)  # TODO: this should be careful
        # self.textEdit_refreshToken.setStyleSheet('QTextEdit{background: yellow}')

        # self.local_already_verified = False
        self.tabWidget.findChild(QTabBar).setVisible(False)
        self.columns = [
            "ID",
            "BROKER",
            "USERNAME",
            "PASSWORD",
            "ACCOUNT_NUMBER",
            "FUTU_HOST",
            "FUTU_PORT",
            "TRADING_PASSWORD",
            "CLIENT_ID",
            "REDIRECT_URI",
            "REFRESH_TOKEN",
            "CONSUMER_KEY",
            "CONSUMER_SECRET"]
        self.broker_list_df = pd.DataFrame(columns=self.columns)
        self.label_12.setOpenExternalLinks(True)
        self.textEdit_refreshToken.wordWrapMode()

        # disable all broker groups initially
        self.groupBox_getAccList.setVisible(False)
        self.groupBox_accList.setVisible(False)
        self.groupBox_tp.setVisible(False)
        self.pushButton_getAccList.setEnabled(False)
        self.clicked_row = None
        self.clicked_model = None

        self.thread = {}

    def connect_slots(self):
        self.broker_comboBox.currentIndexChanged.connect(self.update_display)
        # self.verify_button.clicked.connect(self.verify_local_broker_account)
        self.add_broker_button.clicked.connect(self.add_broker_account)
        self.delete_button.clicked.connect(self.delete_broker_account)
        self.delete_local_button.clicked.connect(self.reset_local_file)
        self.pushButton_getAccList.clicked.connect(self.get_acc_list)

    def check_term(self):
        if self.futu_disclaimer_check.isChecked() == True:
            self.pushButton_getAccList.setEnabled(True)
        else:
            self.pushButton_getAccList.setEnabled(False)

    def get_acc_list(self):
        self.groupBox_accList.setVisible(False)
        broker = self.broker_comboBox.currentText()
        if "FUTU" in broker:
            futu_host = str(self.futu_host_edit.text())
            futu_port = int(self.futu_port_spin.value())
            broker_obj = FutuAcc(
                broker=broker, futu_host=futu_host, futu_port=futu_port
            )

        elif broker == "TD Ameritrade":
            clientID = self.lineEdit_clientID.text()
            redirect_uri = self.lineEdit_redirect_uri.text()
            refresh_token = self.textEdit_refreshToken.toPlainText()
            broker_obj = TDAcc(
                broker=broker,
                client_id=clientID,
                redirect_uri=redirect_uri,
                refresh_token=refresh_token,
            )
        elif broker == "Interactive Brokers":
            username = self.lineEdit_username.text()
            password = self.lineEdit_password.text()
            broker_obj = IBAcc(broker=broker, username=username, password=password)

        elif broker == "E*Trade":
            username = self.lineEdit_userEtrade.text()
            password = self.lineEdit_passEtrade.text()
            consumer_key = self.textEdit_key.toPlainText()
            consumer_secret = self.textEdit_secret.toPlainText()
            broker_obj = ETradeAcc(broker=broker, username=username, password=password, consumer_key=consumer_key,
                                   consumer_secret=consumer_secret)
        try:
            self.thread[-1].stop()
        except Exception:
            pass
        self.thread[-1] = AccListThread(broker_obj=broker_obj)
        self.thread[-1].start()
        self.thread[-1].signal_acc_df.connect(self.on_acc_get)
        self.thread[-1].failed.connect(self.on_acc_getter_failed)

    def on_acc_getter_failed(self, msg):
        self.thread[-1].stop()
        QMessageBox.critical(
            self,
            f"{BT.acc_getter_failed[self.LANGUAGE][0]}",
            msg,
        )

    def on_acc_get(self, acc_df):
        self.thread[-1].stop()
        if len(acc_df.index) == 0:
            QMessageBox.critical(self, "获取账户失败", "账户列表中没有实盘账户")
            return
        if "FUTU" in acc_df["broker"][0]:
            acc_df["acc_id"] = acc_df["acc_id"].apply(lambda x: str(x))
            self.tableView_accList.setModel(
                pandasModel(acc_df[["acc_id", "trdmarket_auth"]])
            )
        elif acc_df["broker"][0] == "TD Ameritrade":
            self.tableView_accList.setModel(pandasModel(acc_df[["accountId", "type"]]))
        elif acc_df["broker"][0] == "Interactive Brokers":
            self.tableView_accList.setModel(pandasModel(acc_df[["Account ID"]]))
        elif acc_df["broker"][0] == "E*Trade":
            self.tableView_accList.setModel(pandasModel(acc_df[["accountId"]]))

        self.acc_df = acc_df

        self.groupBox_accList.setVisible(True)
        self.add_broker_button.setEnabled(True)
        self.tableView_accList.setSelectionBehavior(QTableView.SelectRows)
        self.tableView_accList.clicked.connect(self.on_acc_clicked)
        self.tableView_accList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_accList.resizeColumnsToContents()

    def on_acc_clicked(self, clickedIndex):
        self.clicked_row = clickedIndex.row()
        # self.clicked_model = clickedIndex.model()

    def update_display(self):
        self.add_broker_button.setEnabled(False)
        if "FUTU" in self.broker_comboBox.currentText():
            self.futu_disclaimer_check.stateChanged.connect(self.check_term)
            self.tabWidget.setCurrentIndex(1)
            self.groupBox_getAccList.setVisible(True)
            self.groupBox_accList.setVisible(False)
            self.groupBox_tp.setVisible(True)
        else:
            try:
                self.futu_disclaimer_check.stateChanged.disconnect()
            except Exception:
                pass
            if self.broker_comboBox.currentText() == "TD Ameritrade":
                self.tabWidget.setCurrentIndex(3)
                self.pushButton_getAccList.setEnabled(True)
                self.groupBox_getAccList.setVisible(True)
                self.groupBox_accList.setVisible(False)
                self.groupBox_tp.setVisible(False)
            elif self.broker_comboBox.currentText() == "Interactive Brokers":
                self.tabWidget.setCurrentIndex(4)
                self.pushButton_getAccList.setEnabled(True)
                self.groupBox_getAccList.setVisible(True)
                self.groupBox_tp.setVisible(False)
            elif self.broker_comboBox.currentText() == "E*Trade":
                self.tabWidget.setCurrentIndex(5)
                self.pushButton_getAccList.setEnabled(True)
                self.groupBox_getAccList.setVisible(True)
                self.groupBox_tp.setVisible(False)

            else:
                self.tabWidget.setCurrentIndex(0)
                self.groupBox_getAccList.setVisible(False)
                self.groupBox_accList.setVisible(False)
                self.groupBox_tp.setVisible(False)

    def add_broker_account(self):
        # if self.local_already_verified == False:
        #     self.verify_local_broker_account()
        broker = self.broker_comboBox.currentText()
        if broker == "":
            QMessageBox.critical(self, "账户错误", "请选择一个券商")
            return

        try:
            self.acc_df
        except AttributeError:
            QMessageBox.critical(self, "账户错误", "没有交易账户")
            return
        if len(self.acc_df) < 1:
            QMessageBox.critical(self, "账户错误", "没有交易账户")
            return
        elif self.clicked_row == None:
            QMessageBox.critical(self, "账户错误", "请选择一个账户")
            return
        else:
            if "FUTU" in broker:
                account_number = self.acc_df.iloc[self.clicked_row]["acc_id"]
            elif broker == "TD Ameritrade":
                account_number = self.acc_df.iloc[self.clicked_row]["accountId"]
            elif broker == "Interactive Brokers":
                account_number = self.acc_df.iloc[self.clicked_row]["Account ID"]
            elif broker == "E*Trade":
                account_number = self.acc_df.iloc[self.clicked_row]["accountId"]

        logging.info(broker)
        logging.info(account_number)
        num_existed_account = len(self.broker_list_df)
        logging.info(num_existed_account)
        # num_existed_broker = len(self.broker_list_df[self.broker_list_df['broker'] == broker])
        if self.aurora_account.account_tier == "standard":
            if num_existed_account > 0:
                QMessageBox.critical(
                    self,
                    "达到账户限制",
                    "请升级账户",
                )
                return

        elif self.aurora_account.account_tier == "VIP":
            existed_broker = self.broker_list_df["BROKER"].unique()
            if len(existed_broker) == 1 and broker not in existed_broker:
                QMessageBox.critical(
                    self,
                    "存在不同券商账户",
                    "请升级账户",
                )
                return
            if len(existed_broker) > 1:
                self.reset_local_file()
                QMessageBox.critical(
                    self,
                    "存在不同券商账户",
                    "本地账户重置",
                )
                return

        elif self.aurora_account.account_tier == "SVIP":
            if num_existed_account > 9:
                QMessageBox.critical(
                    self,
                    "达到账户限制",
                    "请升级账户",
                )
                return

        else:
            QMessageBox.critical(
                self,
                "请联系Aurora",
                "您的账户等级有误",
            )
            return
        broker_acc = self.broker_account_generator(broker, account_number)
        self.authenticate(broker_acc, -2)

    def fetch_local_accounts(self):
        if os.path.exists(r"temp/broker_list.csv") == False:
            self.local_broker_list_df = pd.DataFrame(columns=self.columns)
        else:
            self.local_broker_list_df = pd.read_csv(
                r"temp/broker_list.csv",
                header=0,
                dtype={
                    "ID": "Int64",
                    "BROKER": object,
                    "USERNAME": object,
                    "PASSWORD": object,
                    "ACCOUNT_NUMBER": object,
                    "FUTU_HOST": object,
                    "FUTU_PORT": "Int64",
                    "TRADING_PASSWORD": object,
                    "CLIENT_ID": object,
                    "REDIRECT_URI": object,
                    "REFRESH_TOKEN": object,
                    "CONSUMER_KEY": object,
                    "CONSUMER_SECRET": object,

                },
            )
            if self.local_broker_list_df.columns.tolist() != self.columns:
                self.reset_local_file()

    def verify_local_broker_account(self):
        # if self.local_already_verified == False:
        self.fetch_local_accounts()

        num_existed_broker = len(self.local_broker_list_df)
        self.max_index = num_existed_broker - 1
        if self.aurora_account.account_tier == "standard":
            if num_existed_broker > 2:
                self.broker_list_df = self.local_broker_list_df.iloc[0:0]
                QMessageBox.critical(self, "账户数量错误", "请升级账户")
                return
        elif self.aurora_account.account_tier == "VIP":
            if num_existed_broker > 5:
                self.broker_list_df = self.local_broker_list_df.iloc[0:0]
                QMessageBox.critical(self, "账户数量错误", "请升级账户")
                return
        elif self.aurora_account.account_tier == "SVIP":
            if num_existed_broker > 10:
                self.broker_list_df = self.local_broker_list_df.iloc[0:0]
                QMessageBox.critical(self, "账户数量错误", "请升级账户")
                return
        # self.local_already_verified = True
        for index, account in self.local_broker_list_df.iterrows():
            # self.broker_list_df = self.broker_list_df.drop(index=index)
            if "FUTU" in account["BROKER"]:
                broker_account = FutuAcc(
                    broker=str(account["BROKER"]),
                    account_number=str(account["ACCOUNT_NUMBER"]),
                    futu_host=str(account["FUTU_HOST"]),
                    futu_port=int(account["FUTU_PORT"]),
                    trading_password=str(account["TRADING_PASSWORD"]),
                )
            elif account["BROKER"] == "TD Ameritrade":
                broker_account = TDAcc(
                    broker=str(account["BROKER"]),
                    client_id=str(account["CLIENT_ID"]),
                    redirect_uri=str(account["REDIRECT_URI"]),
                    refresh_token=str(account["REFRESH_TOKEN"]),
                    account_number=str(account["ACCOUNT_NUMBER"]),
                )
            elif account["BROKER"] == "Interactive Brokers":
                broker_account = IBAcc(
                    broker=str(account["BROKER"]),
                    username=str(account["USERNAME"]),
                    password=str(account["PASSWORD"]),
                    account_number=str(account["ACCOUNT_NUMBER"]),
                )
            elif account["BROKER"] == "E*Trade":
                broker_account = ETradeAcc(
                    broker=str(account["BROKER"]),
                    username=str(account["USERNAME"]),
                    password=str(account["PASSWORD"]),
                    account_number=str(account["ACCOUNT_NUMBER"]),
                    consumer_key=str(account["CONSUMER_KEY"]),
                    consumer_secret=str(account["CONSUMER_SECRET"]),
                )

            else:
                QMessageBox.critical(self, "错误", "存在未知券商")
                return
            self.authenticate(broker_account, index)
            # self.broker_list_df.drop_duplicates()

    def broker_account_generator(self, broker, account_number, account_id_key=None):
        """
        generate broker account object for each broker with corresponding class
        """
        if "FUTU" in broker:
            futu_host = str(self.futu_host_edit.text())
            futu_port = int(self.futu_port_spin.value())
            trading_password = str(self.trading_password_edit.text())
            broker_account = FutuAcc(
                broker=broker,
                account_number=account_number,
                futu_host=futu_host,
                futu_port=futu_port,
                trading_password=trading_password,
            )
        elif broker == "TD Ameritrade":
            broker_account = TDAcc(
                broker=broker,
                account_number=account_number,
                client_id=self.lineEdit_clientID.text(),
                redirect_uri=self.lineEdit_redirect_uri.text(),
                refresh_token=self.textEdit_refreshToken.toPlainText(),
            )
        elif broker == "Interactive Brokers":
            broker_account = IBAcc(
                broker=broker,
                username=self.lineEdit_username.text(),
                password=self.lineEdit_password.text(),
                account_number=account_number,
            )
        elif broker == "E*Trade":
            broker_account = ETradeAcc(
                broker=broker,
                username=self.lineEdit_userEtrade.text(),
                password=self.lineEdit_passEtrade.text(),
                consumer_key=self.textEdit_key.toPlainText(),
                consumer_secret=self.textEdit_secret.toPlainText(),
            )
        self.trading_password_edit.clear()
        return broker_account

    def authenticate(self, broker_acc, id):
        # try:
        #     self.thread[1].stop()
        #     print("stop", "\n")
        # except Exception:
        #     pass
        self.setEnabled(False)
        # QMessageBox.information(self, "请稍候", "正在验证登录本地账号")
        self.thread[id] = AuthThread(broker_obj=broker_acc, id=id)
        self.thread[id].start()
        self.thread[id].authenticated.connect(self.on_acc_authenticated)
        self.thread[id].failed.connect(self.on_authenticated_failed)

    def on_authenticated_failed(self, msg):
        if msg["id"] == self.max_index:
            self.setEnabled(True)
        self.thread[msg["id"]].stop()
        QMessageBox.critical(self, "账号验证失败", msg["content"])

    def on_acc_authenticated(self, msg):
        if msg["id"] == self.max_index:
            self.setEnabled(True)
        thread_id = msg["id"]
        self.thread[thread_id].stop()
        broker_obj = msg["broker_obj"]
        if self.same_broker_account_detected(
            broker_obj.broker, broker_obj.account_number
        ):
            QMessageBox.critical(
                self,
                "存在相同账户",
                "请添加其他账户",
            )
            return
        if len(self.broker_list_df) == 0:
            id = 1
        else:
            id = int(self.broker_list_df.ID.max()) + 1
        QMessageBox.information(
            self,
            "成功",
            f"成功添加{broker_obj.account_number}",
        )
        self.authenticated.emit(broker_obj)
        if "FUTU" in broker_obj.broker:
            new_broker_account = pd.DataFrame(
                [
                    [
                        id,
                        broker_obj.broker,
                        "",
                        broker_obj.password,
                        broker_obj.account_number,
                        broker_obj.futu_host,
                        broker_obj.futu_port,
                        broker_obj.trading_password,
                        "",
                        "",
                        "",
                        "",
                        "",
                    ]
                ]
            )

        elif broker_obj.broker == "TD Ameritrade":
            new_broker_account = pd.DataFrame(
                [
                    [
                        id,
                        broker_obj.broker,
                        "",
                        broker_obj.password,
                        broker_obj.account_number,
                        "",
                        "",
                        "",
                        broker_obj.client_id,
                        broker_obj.redirect_uri,
                        broker_obj.refresh_token,
                        "",
                        "",
                    ]
                ]
            )
        elif broker_obj.broker == "Interactive Brokers":
            new_broker_account = pd.DataFrame(
                [
                    [
                        id,
                        broker_obj.broker,
                        broker_obj.username,
                        broker_obj.password,
                        broker_obj.account_number,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ]
                ]
            )
        elif broker_obj.broker == "E*Trade":
            new_broker_account = pd.DataFrame(
                [
                    [
                        id,
                        broker_obj.broker,
                        broker_obj.username,
                        broker_obj.password,
                        broker_obj.account_number,
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        broker_obj.consumer_key,
                        broker_obj.consumer_secret,
                    ]
                ]
            )

        new_broker_account.columns = self.columns
        self.broker_list_df = pd.concat([self.broker_list_df, new_broker_account])
        self.set_broker_view_model(
            pandasModel(self.broker_list_df[["ID", "BROKER", "ACCOUNT_NUMBER"]])
        )

    def set_broker_view_model(self, model):
        self.broker_table_view.setModel(model)
        self.broker_table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.broker_table_view.horizontalHeader().setFont(QFont('Times New Roman',8))
        # self.broker_table_view.setFont(QFont('Times New Roman',8))
        self.broker_table_view.resizeColumnsToContents()
        self.broker_list_df.to_csv(r"temp/broker_list.csv", index=False, header=True)

    # https://stackoverflow.com/questions/69333824/python-pandas-qtableview-how-to-delete-selected-rows-and-refresh-qtableview

    def delete_broker_account(self):
        if self.id_edit.text().isdigit():
            id = int(self.id_edit.text())
        else:
            QMessageBox.critical(self, "没有输入", "请输入ID")
            return
        selected_account = self.broker_list_df.loc[
            self.broker_list_df["ID"] == id
        ].reset_index()
        if len(selected_account) == 1:
            selected_account_obj = BrokerBase(
                broker=selected_account.BROKER[0],
                account_number=selected_account.ACCOUNT_NUMBER[0],
            )

            self.deleted.emit(selected_account_obj)
            self.broker_list_df = self.broker_list_df.loc[
                self.broker_list_df["ID"] != id
            ]
            self.set_broker_view_model(
                pandasModel(self.broker_list_df[["ID", "BROKER", "ACCOUNT_NUMBER"]])
            )

        else:
            QMessageBox.critical(self, "删除失败", "请确认ID后重试")

    def reset_local_file(self):
        if QMessageBox.Yes == QMessageBox.question(
            self,
            "重置",
            "请确认并重启软件",
            QMessageBox.Yes,
            QMessageBox.No,
        ):
            self.broker_list_df = pd.DataFrame(
                columns=self.columns,
            )
            self.broker_list_df.to_csv(
                r"temp/broker_list.csv", index=False, header=True
            )
            self.close()

    def same_broker_account_detected(self, broker, account_number):
        logging.info(self.broker_list_df)
        if (
            len(
                self.broker_list_df.loc[
                    (self.broker_list_df["BROKER"] == broker)
                    & (self.broker_list_df["ACCOUNT_NUMBER"] == account_number)
                ]
            )
            > 0
        ):
            return True
        else:
            return False

    def load_layout(self):
        file_path = r"temp/layout.json"
        if os.path.exists(file_path) == False:
            pass
        else:
            with open(file_path, "r") as layoutF:
                layout_obj = json.load(layoutF)
            if "broker_window" in layout_obj:
                self.move(
                    layout_obj["broker_window"]["x"], layout_obj["broker_window"]["y"]
                )
                self.resize(
                    layout_obj["broker_window"]["w"], layout_obj["broker_window"]["h"]
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    BrokerWindow.aurora_account.account_tier = "SVIP"
    w = BrokerWindow()
    sys.exit(app.exec_())
