from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
import logging
import pandas as pd
from datetime import datetime
from pytz import timezone
from utils.database import AuroraDB

logging.basicConfig(level=logging.DEBUG)


class PositionThread(QThread):

    failed = pyqtSignal()
    signal_acc_pos = pyqtSignal()
    signal_acc_asset = pyqtSignal()

    def __init__(self, parent=None, broker_list=[], aurora_account=None):
        super(PositionThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_list = broker_list
        self.aurora_account = aurora_account

    def run(self):
        logging.info("start position thread")
        error_counter = 0
        while error_counter < 10:
            for broker_obj in self.broker_list:
                try:
                    # jimmy 降低 futu 请求频率, 否则 get_acc_pos 与 get_acc_asset 间隔太短报错
                    # time.sleep(4)
                    acc_pos = broker_obj.get_acc_pos()
                    time.sleep(5)

                except Exception as e:
                    logging.error(str(error_counter))
                    logging.error(e, exc_info=True)
                    error_counter += 1
                    time.sleep(1)
                else:
                    if acc_pos:
                        self.signal_acc_pos.emit()
                        # self.sync_to_db(broker_obj)
                try:
                    # jimmy 降低 futu 请求频率
                    acc_asset = broker_obj.get_acc_asset()
                    time.sleep(5)
                except Exception as e:
                    logging.error(str(error_counter))
                    logging.error(e, exc_info=True)
                    error_counter += 1
                    time.sleep(1)
                else:
                    if acc_asset:
                        self.signal_acc_asset.emit()
            time.sleep(10)
        self.failed.emit()

    def stop(self):
        self._running = False
        logging.info("Stop pos thread...")
        self.terminate()


class Sync2DBThread(QThread):

    failed = pyqtSignal()

    def __init__(self, parent=None, broker_list=[], aurora_account=None, db_list=[]):
        super(Sync2DBThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_list = broker_list
        self.aurora_account = aurora_account
        self.db_list = db_list

    def run(self):
        error_counter = 0
        while error_counter < 5:
            for broker_obj in self.broker_list:
                try:
                    logging.info("start sync position thread")
                    logging.info(broker_obj.account_number)

                    # jimmy 降低 futu 请求频率, 否则 get_acc_pos 与 get_acc_asset 间隔太短报错
                    time.sleep(5)
                    acc_pos = broker_obj.get_acc_pos()
                    time.sleep(5)
                    acc_asset = broker_obj.get_acc_asset()
                except Exception as e:
                    logging.error(e, exc_info=True)
                    logging.error(str(error_counter))
                    error_counter += 1
                    time.sleep(1)
                else:
                    if acc_pos:
                        try:
                            self.sync_to_db(broker_obj)
                        except Exception as e:
                            logging.error(e, exc_info=True)
                            logging.error(str(error_counter))
                            error_counter += 1
                            time.sleep(1)
            time.sleep(10)
        self.failed.emit()

    def stop(self):
        self._running = False
        logging.info("stop sync position thread")
        self.terminate()

    def sync_to_db(self, broker_obj):
        self.db_obj = AuroraDB(self.db_list)
        pos_db = broker_obj.position.loc[
            :, ["code", "cost_price", "qty", "nominal_price"]
        ]
        if pos_db.shape[0] == 0:
            pass
        else:
            pos_db.rename(
                columns={"cost_price": "cost", "nominal_price": "current_price"},
                inplace=True,
            )
            pos_db.reset_index(drop=True, inplace=True)
            pos_db.loc[:, "username"] = self.aurora_account.username
            pos_db.loc[:, "account"] = str(broker_obj)
            # 时区转换, 将上传时间统一为北京时间
            pos_db.loc[:, "datetime"] = datetime.now(
                timezone("Asia/Shanghai")
            ).strftime("%Y-%m-%d %H:%M:%S")

            # time.sleep(2)  # 频繁访问数据库不知道会不会有影响
            self.db_obj.insert_position(pos_db)

        cash_db = pd.DataFrame(
            data={
                "username": self.aurora_account.username,
                "account": str(broker_obj),
                "cash": str(broker_obj.cash),
                "datetime": datetime.now(timezone("Asia/Shanghai")).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            },
            index=[0],
        )
        time.sleep(2)

        self.db_obj.insert_cash(cash_db)
