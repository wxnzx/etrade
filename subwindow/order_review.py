import sys
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from UI.UI_order_review import Ui_OrderReview
import logging

logging.basicConfig(level=logging.INFO)


class OrderReviewWindow(QWidget, Ui_OrderReview):
    def __init__(self, order_dict):
        super().__init__()
        self.setupUi(self)
        self.order_dict = order_dict

        self.setWindowModality(Qt.ApplicationModal)
        self.initialize()

    def initialize(self):

        self.textBrowser_orderDetail.setFontPointSize(14)
        self.textBrowser_orderDetail.setFontWeight(QFont.Bold)
        if self.order_dict:
            if self.order_dict['side'] == 'BUY':
                self.textBrowser_orderDetail.setStyleSheet('QTextBrowser{background: green}')
            else:
                self.textBrowser_orderDetail.setStyleSheet('QTextBrowser{background: red}')
            order_info_check_str = ""
            for key, value in self.order_dict.items():
                order_info_check_str += str(key)
                order_info_check_str += ": "
                order_info_check_str += str(value)
                order_info_check_str += "\n"
            self.textBrowser_orderDetail.setText(order_info_check_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OrderReviewWindow({'order': 'dict', 'price': 10, 'side': 'BUY'})
    w.show()
    sys.exit(app.exec_())
