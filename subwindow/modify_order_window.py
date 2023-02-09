import sys
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
)
from PyQt5.QtCore import Qt

from UI.UI_modify_order import Ui_Form
import logging

logging.basicConfig(level=logging.INFO)


class ModifyOrderWindow(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("QLineEdit:read-only{background: palette(window);}")
        self.order_id = str(args[0])
        self.code = str(args[1])
        self.order_type = str(args[2])
        self.trd_side = str(args[3])
        self.qty = int(args[4])
        self.price = float(args[5])
        if self.order_type == "STOP" or self.order_type == "STOP LIMIT":
            self.aux_price = float(args[6])
        self.time_in_force = str(args[7])
        self.market_session = str(args[8])
        self.broker = args[9]
        self.setWindowModality(Qt.ApplicationModal)
        self.initialize()
        self.show()

    def initialize(self):
        self.lineEdit_orderID.setText(self.order_id)
        self.lineEdit_orderType.setText(self.order_type)
        self.lineEdit_side.setText(self.trd_side)
        self.lineEdit_sym.setText(self.code)
        self.spinBox_qty.setValue(self.qty)
        self.doubleSpinBox_price.setValue(self.price)
        if self.order_type == "STOP" or self.order_type == "STOP LIMIT":
            self.doubleSpinBox_sprice.setValue(self.aux_price)
        self.lineEdit_tif.setText(self.time_in_force)
        self.lineEdit_session.setText(self.market_session)
        self.dateEdit_gtd.setEnabled(False)

        self.pushButton_cancel.setStyleSheet(
            "QPushButton{background: gray; font-size:22px}"
        )

        if self.trd_side == "BUY":
            self.pushButton_modify.setStyleSheet(
                "QPushButton{background: rgb(40, 202, 89); font-size:22px}"
            )
        else:
            self.pushButton_modify.setStyleSheet(
                "QPushButton{background: rgb(241, 73, 82); font-size:22px}"
            )

        # change UI for each broker
        # if "FUTU" in self.broker:
        #     self.lineEdit_tif.setEnabled(False)
        #     self.lineEdit_session.setEnabled(False)
        #     self.dateEdit_gtd.setEnabled(False)
        # elif "TD" in self.broker:
        #     self.lineEdit_tif.setEnabled(True)
        #     self.lineEdit_session.setEnabled(True)
        #     self.dateEdit_gtd.setEnabled(False)
        # elif "Interactive Brokers" in self.broker:
        #     self.lineEdit_tif.setEnabled(True)
        #     self.lineEdit_session.setEnabled(True)
        #     self.dateEdit_gtd.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ModifyOrderWindow(1, 2, 3, 4, 5, 6, 7)
    sys.exit(app.exec_())
