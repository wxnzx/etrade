from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import logging
import time
from datetime import datetime
from pytz import timezone  # 时区转换
import pandas as pd
from utils.database import AuroraDB

logging.basicConfig(level=logging.DEBUG)


class Sync2DBThread(QThread):

    failed = pyqtSignal()

    def __init__(self, parent=None, aurora_account=None, db_list=None):
        super(Sync2DBThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.aurora_account = aurora_account
        self.db_list = db_list

    def run(self):
        logging.info("start sync acc login thread")
        error_counter = 0
        while error_counter < 5:
            try:
                self.sync_to_db()
            except Exception as e:
                logging.error(error_counter)
                logging.error(e, exc_info=True)
                error_counter += 1
                time.sleep(1)
            else:
                time.sleep(60)
        self.failed.emit()

    def sync_to_db(self):
        self.db_obj = AuroraDB(self.db_list)
        acc_info = pd.DataFrame(
            {
                "username": [self.aurora_account],
                # jimmy 登录时间统一转为中国时间
                "datetime": [
                    datetime.now(timezone("Asia/Shanghai")).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ],
            }
        )
        # acc_info['username'] = self.aurora_account
        # acc_info["datetime"] = datetime.today()
        self.db_obj.insert_account(acc_info)

    def stop(self):
        self._running = False
        logging.info("stop sync acc login thread")
        self.terminate()
