from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QObject
import time
import logging
import pandas as pd
import futu

logging.basicConfig(level=logging.DEBUG)


class PlaceOrderThread(QThread):

    failed = pyqtSignal(str)
    signal_order_return = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None, broker_obj=None, order_info_dict={}):
        super(PlaceOrderThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_obj = broker_obj
        self.order_info_dict = order_info_dict

    def run(self):
        try:
            logging.info("start place order thread")
            logging.info(self.broker_obj.account_number)
            ret, data = self.broker_obj.place_order(self.order_info_dict)
        except Exception as e:
            logging.error(e, exc_info=True)
            self.failed.emit(str(e))
        else:
            if ret == "OK":
                self.signal_order_return.emit(data)
            elif ret == "Error":
                self.failed.emit(f"下单失败:{data}")
            elif ret == "UnlockError":
                self.failed.emit("解锁失败")

    def stop(self):
        self._running = False
        logging.info("Stop place order thread...")
        self.terminate()
