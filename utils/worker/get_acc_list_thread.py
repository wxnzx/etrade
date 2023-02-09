from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


class AccListThread(QThread):

    failed = pyqtSignal(str)
    signal_acc_df = pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None, broker_obj=None):
        super(AccListThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_obj = broker_obj

    def run(self):
        logging.info("start AccListThread")
        try:
            ret, data = self.broker_obj.get_acc_list()
        except Exception as e:
            logging.error(e, exc_info=True)
            # TD refresh token 过期错误时弹出提示 (NOT REVIEWED)
            if "TD" in str(self.broker_obj):
                self.failed.emit("Could not authenticate 请检查refresh token是否过期")
            else:
                self.failed.emit(str(e))
            time.sleep(1)
        else:
            if ret == "OK":
                data["broker"] = self.broker_obj.broker
                logging.info(data)
                self.signal_acc_df.emit(data)
            else:
                self.failed.emit(data)

    def stop(self):
        self._running = False
        logging.info("Stop AccListThread")
        self.terminate()
