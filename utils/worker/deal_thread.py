from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


class DealThread(QThread):

    failed = pyqtSignal()
    signal_acc_deals = pyqtSignal(dict)

    def __init__(self, parent=None, broker_list=[], today=True, date=[]):
        super(DealThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_list = broker_list

    def run(self):
        error_counter = 0
        while error_counter < 5:
            for broker_obj in self.broker_list:
                try:
                    logging.info("start order detail thread")
                    logging.info(broker_obj.account_number)
                    acc_orders = broker_obj.get_acc_deals()
                    acc_orders.insert(0, column="account", value=str(broker_obj))
                except Exception as e:
                    logging.error(error_counter)
                    logging.error(e, exc_info=True)
                    error_counter += 1
                    time.sleep(1)

                else:
                    # acc_str = f"{str(broker_obj.broker)}-{str(broker_obj.username)}"
                    # acc_orders_dict = {'index':acc_str,'orders':acc_orders}
                    acc_orders_dict = {"index": str(broker_obj), "orders": acc_orders}
                    self.signal_acc_orders.emit(acc_orders_dict)
            time.sleep(10)
        self.failed.emit()

    def stop(self):
        self._running = False
        logging.info("Stop order detail thread...")
        self.terminate()
