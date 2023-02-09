from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QEvent
import sys
from UI.UI_level_one_window import Ui_Form
from datetime import date
import os
from account import AuroraAccount
from subwindow.order_review import OrderReviewWindow
from utils.worker.place_order_thread import PlaceOrderThread
from utils.worker.quote_thread import QuoteThread
from UI.data_model import pandasModel
import pandas as pd
import json
import logging


logging.basicConfig(level=logging.INFO)


class LevelOne(QWidget, Ui_Form):
    server_ip = None
    server_port = None
    signal_order_info = pyqtSignal(str)
    signal_streaming_failed = pyqtSignal()
    # level_one_data_rqst = qtc.pyqtSignal(str)
    broker_list = []  # a list of BrokerAccount
    aurora_account = None
    token = None
    socket = None
    LANGUAGE = "CN"
    Y = 70

    def __init__(self, layout_number=-1):
        super().__init__()
        self.setupUi(self)

        # jimmy
        self.order_review = OrderReviewWindow({})
        self.order_info_dict = {}
        self.layout_number = layout_number

        self.initialize()
        self.connect_slots()
        self.show()

    def initialize(self):
        self.resize(900, 316)
        self.move(1210, 70)
        if self.layout_number >= 0:
            self.load_layout()

        self._socket_ready = False
        self.setWindowTitle("Level I")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.pushButton_buy.setStyleSheet(
            "QPushButton{"
            "background-color: rgb(35, 177, 77);"
            "font-size:26px;"
            "}"
            "QPushButton::hover{"
            "background-color: rgb(40, 202, 89);"
            "font-size:26px;"
            "}"
        )
        self.pushButton_sell.setStyleSheet(
            "QPushButton{"
            "background-color: rgb(237, 27, 36);"
            "font-size:26px;"
            "}"
            "QPushButton::hover{"
            "background-color: rgb(241, 73, 82);"
            "font-size:26px;"
            "}"
        )

        self.thread = {}
        if len(self.broker_list) != 0:
            for broker_account in self.broker_list:
                self.comboBox_acc.addItem(str(broker_account))
            # for broker_account in self.broker_list:
            #     if (
            #         f"{broker_account.broker}" == "FUTUBULL 富途牛牛"
            #         or f"{broker_account.broker}" == "FUTU MOOMOO"
            #     ):
            #         self.quote_broker_obj = broker_account
        self.clear_ui()
        # self.start_server_connection_worker()

    def connect_slots(self):
        self.comboBox_acc.currentIndexChanged.connect(self.on_acc_changed)
        self.comboBox_ptype.currentIndexChanged.connect(self.on_order_type_changed)
        self.comboBox_tif.currentIndexChanged.connect(self.on_TIF_changed)
        self.pushButton_buy.clicked.connect(self.buy_on_send)
        self.pushButton_sell.clicked.connect(self.sell_on_send)
        self.pushButton_clear.clicked.connect(self.clear_ui)
        self.lineEdit_sym.returnPressed.connect(self.get_quote)

    def get_quote(self):
        try:
            self.thread[1].stop()
        except Exception as e:
            pass
        # if self.quote_broker_obj:
        self.thread[1] = QuoteThread(
            symbol=self.lineEdit_sym.text().upper(),
        )
        self.thread[1].start()
        self.thread[1].signal_quote.connect(self.on_quote_received)
        self.thread[1].failed.connect(self.on_quote_failed)

    def on_quote_received(self, quote):
        self.tableView.setModel(pandasModel(quote))
        self.tableView.resizeColumnsToContents()

    def on_quote_failed(self):
        failed_quote = pd.DataFrame({"状态": ["失败"], "信息": ["该股票不支持获取报价"]})
        self.tableView.setModel(pandasModel(failed_quote))
        self.tableView.resizeColumnsToContents()
        self.thread[1].stop()

    def on_acc_changed(self):
        self.setWindowTitle(self.comboBox_acc.currentText())

        # TODO: change layout details based on choosen brokerage
        # such as TIF, market session, order type, etc.
        if "FUTU" in self.comboBox_acc.currentText():
            self.comboBox_tif.clear()
            self.comboBox_tif.addItem("DAY")
            self.comboBox_tif.addItem("GTC")
            self.comboBox_session.setEnabled(True)
            self.comboBox_session.clear()
            self.comboBox_session.addItem("REGULAR")
            self.comboBox_session.addItem("EXTENDED")
        elif "TD" in self.comboBox_acc.currentText():
            self.comboBox_tif.clear()
            self.comboBox_tif.addItem("DAY")
            self.comboBox_tif.addItem("GTC")
            self.comboBox_session.setEnabled(True)
            self.comboBox_session.clear()
            self.comboBox_session.addItem("REGULAR")
            self.comboBox_session.addItem("AM")
            self.comboBox_session.addItem("PM")

        elif "Interactive Brokers" in self.comboBox_acc.currentText():
            self.comboBox_tif.clear()
            self.comboBox_tif.addItem("DAY")
            self.comboBox_tif.addItem("GTC")
            self.comboBox_session.setEnabled(True)
            self.comboBox_session.clear()
            self.comboBox_session.addItem("REGULAR")
            self.comboBox_session.addItem("EXTENDED")

        elif "E*Trade" in self.comboBox_acc.currentText():
            self.comboBox_tif.clear()
            self.comboBox_tif.addItem("DAY")
            self.comboBox_tif.addItem("GTD")
            self.comboBox_tif.addItem("GTC")
            self.comboBox_tif.addItem("IOC")
            self.comboBox_tif.addItem("FOK")
            self.comboBox_session.setEnabled(True)
            self.comboBox_session.clear()
            self.comboBox_session.addItem("REGULAR")
            self.comboBox_session.addItem("EXTENDED")

    def on_order_type_changed(self):
        if self.comboBox_ptype.currentText() == "Market":
            self.doubleSpinBox_price.setEnabled(False)
            self.doubleSpinBox_sprice.setEnabled(False)
        elif self.comboBox_ptype.currentText() == "Limit":
            self.doubleSpinBox_price.setEnabled(True)
            self.doubleSpinBox_sprice.setEnabled(False)
        elif self.comboBox_ptype.currentText() == "Stop Limit":
            self.doubleSpinBox_price.setEnabled(True)
            self.doubleSpinBox_sprice.setEnabled(True)
        elif self.comboBox_ptype.currentText() == "Stop":
            self.doubleSpinBox_price.setEnabled(False)
            self.doubleSpinBox_sprice.setEnabled(True)

    def on_TIF_changed(self):
        if self.comboBox_tif.currentText() == "GTD":
            self.dateEdit_gtd.setEnabled(True)
        elif self.comboBox_tif.currentText() == "GTC":
            self.dateEdit_gtd.setEnabled(False)
        elif self.comboBox_tif.currentText() == "DAY":
            self.dateEdit_gtd.setEnabled(False)
        elif self.comboBox_tif.currentText() == "IOC":
            self.dateEdit_gtd.setEnabled(False)
        elif self.comboBox_tif.currentText() == "FOK":
            self.dateEdit_gtd.setEnabled(False)


    def buy_on_send(self):
        side = "BUY"
        self.parse_order_info(side)

    def sell_on_send(self):
        side = "SELL"
        self.parse_order_info(side)

    # jimmy
    def send_order(self):
        self.place_order(self.order_info_dict)
        self.order_review.close()

    def cancel_order(self):
        self.order_review.close()

    def parse_order_info(self, side):
        symbol = (
            self.comboBox_mkt.currentText()
            + "."
            + self.lineEdit_sym.text().strip().upper()  # 删空格
        )
        price = self.doubleSpinBox_price.value()
        quantity = self.spinBox_qty.value()
        account = self.comboBox_acc.currentText()
        price_type = self.comboBox_ptype.currentText()
        stop_price = self.doubleSpinBox_sprice.value()
        time_in_force = self.comboBox_tif.currentText()
        market_session = self.comboBox_session.currentText()
        GTD = self.dateEdit_gtd.date().toString("yyyy-MM-dd")
        AON = self.checkBox_aon.isChecked()
        DNI = self.checkBox_dni.isChecked()
        DNR = self.checkBox_dnr.isChecked()
        emit_dict = {
            "symbol": symbol,
            "side": side,
            "price": price,
            "quantity": quantity,
            "account": account,
            "price type": price_type,
            "stop price": stop_price,
            "time in force": time_in_force,
            "market session": market_session,
            "GTD": GTD,
            # "AON": AON,
            # "DNI": DNI,
            # "DNR": DNR,
        }
        self.order_info_dict = {"status": "order", "content": emit_dict}
        self.order_info_dict["content"]["aurora_account"] = self.aurora_account.username

        # jimmy
        self.order_review = OrderReviewWindow(self.order_info_dict["content"])
        self.order_review.show()
        self.order_review.pushButton_Send.clicked.connect(self.send_order)
        self.order_review.pushButton_Cancel.clicked.connect(self.cancel_order)

        # self.place_order(self.order_info_dict)

    # -------------------------- Place Order --------------------------

    def place_order(self, order_info_dict):

        broker_acc_obj = None
        acc_str = order_info_dict["content"]["account"]
        for broker_acc in self.broker_list:
            if str(broker_acc) == acc_str:
                broker_acc_obj = broker_acc
        if broker_acc_obj:
            logging.info(broker_acc_obj.broker)
            logging.info(broker_acc_obj.account_number)
            self.thread[0] = PlaceOrderThread(
                parent=None,
                broker_obj=broker_acc_obj,
                order_info_dict=self.order_info_dict["content"],
            )
            self.thread[0].start()
            self.thread[0].signal_order_return.connect(self.on_place_order_return)
            self.thread[0].failed.connect(self.on_place_order_failed)
            # broker_acc_obj.place_order(json.loads(order_info_str)['content'])
        else:
            self.on_place_order_failed("该账号不存在")

    def on_place_order_return(self, order_df):
        self.thread[0].stop()
        logging.info(order_df)
        order_return_str = ""
        for key, value in order_df.items():
            order_return_str += str(key)
            order_return_str += ":"
            order_return_str += str(value)
            order_return_str += "\n"
        # msg_box = OrderReturnMessageBox(order_df)
        QMessageBox.information(self, "下单成功", "下单成功!\n请在订单界面查看订单及成交信息")

    def on_place_order_failed(self, msg):
        try:
            self.thread[0].stop()
        except Exception as e:
            pass
        QMessageBox.critical(self, "下单失败", msg)

    def clear_ui(self):
        self.on_acc_changed()

        self.comboBox_mkt.setCurrentText("US")
        self.lineEdit_sym.setText("")
        self.doubleSpinBox_price.setValue(0.00)
        self.spinBox_qty.setValue(0)
        self.comboBox_ptype.setCurrentText("Limit")
        self.spinBox_qty.setEnabled(True)
        self.doubleSpinBox_sprice.setEnabled(False)
        self.comboBox_tif.setCurrentText("DAY")
        self.comboBox_session.setCurrentText("REGULAR")
        self.dateEdit_gtd.setDate(date.today())
        self.dateEdit_gtd.setEnabled(False)
        self.checkBox_aon.setChecked(False)
        self.checkBox_dni.setChecked(False)
        self.checkBox_dnr.setChecked(False)
        self.checkBox_aon.setEnabled(False)
        self.checkBox_dni.setEnabled(False)
        self.checkBox_dnr.setEnabled(False)

    # jimmy
    def load_layout(self):
        file_path = r"temp/layout.json"
        if os.path.exists(file_path) == False:
            pass
        else:
            with open(file_path, "r") as layoutF:
                layout_obj = json.load(layoutF)
            if "level_one_window" in layout_obj:
                if len(layout_obj["level_one_window"]) >= self.layout_number:
                    self.move(
                        layout_obj["level_one_window"][self.layout_number]["x"],
                        layout_obj["level_one_window"][self.layout_number]["y"],
                    )
                    self.resize(
                        layout_obj["level_one_window"][self.layout_number]["w"],
                        layout_obj["level_one_window"][self.layout_number]["h"],
                    )

    def changeEvent(self, event) -> None:

        if event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                self.setStyleSheet("QWidget{background: rgb(220, 254, 255)}")
            else:
                self.setStyleSheet("QWidget{background: white}")

    def closeEvent(self, event):
        for key, val in self.thread.items():
            val.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = AuroraAccount(username="a")
    LevelOne.aurora_account = a
    LevelOne.broker_list.append()
    level_one = LevelOne()

    sys.exit(app.exec_())
