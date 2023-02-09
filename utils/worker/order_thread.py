from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import time
import logging
import pandas as pd
from utils.database import AuroraDB
from datetime import datetime
from pytz import timezone

logging.basicConfig(level=logging.DEBUG)


class OrderThread(QThread):

    failed = pyqtSignal()
    signal_acc_orders = pyqtSignal(dict)

    def __init__(
        self,
        parent=None,
        aurora_account=None,
        broker_list=[],
        order=True,
        today=True,
        date=[],
    ):
        super(OrderThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_list = broker_list
        self.order = order
        self.today = today
        self.date = date

    def run(self):
        error_counter = 0
        while error_counter < 5:
            for broker_obj in self.broker_list:
                try:
                    logging.info("start order thread")
                    logging.info(broker_obj.account_number)
                    if self.order == True and self.today == True:
                        acc_orders = broker_obj.get_today_orders()
                    elif self.order == True and self.today == False:
                        acc_orders = broker_obj.get_history_orders(
                            self.date[0], self.date[1]
                        )
                    elif self.order == True and self.today == None:
                        acc_orders = broker_obj.get_active_orders()
                    elif self.order == False and self.today == True:
                        acc_orders = broker_obj.get_today_deals()
                    elif self.order == False and self.today == False:
                        acc_orders = broker_obj.get_history_deals(
                            self.date[0], self.date[1]
                        )
                    acc_orders.insert(0, column="account", value=str(broker_obj))
                except Exception as e:
                    logging.error(str(error_counter))
                    logging.error(e, exc_info=True)
                    error_counter += 1
                    time.sleep(1)
                else:
                    acc_orders_dict = {"index": str(broker_obj), "orders": acc_orders}
                    self.signal_acc_orders.emit(acc_orders_dict)
            time.sleep(10)
        self.failed.emit()

    def stop(self):
        self._running = False
        logging.info("Stop order thread...")
        self.terminate()


class CancelOrderThread(QThread):
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None, broker_obj=None, order_id=None):
        super(CancelOrderThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_obj = broker_obj
        self.order_id = order_id

    def run(self):
        try:
            logging.info("start cancel order thread")
            data = self.broker_obj.cancel_order(self.order_id)
        except Exception as e:
            if str(e) == "此订单不支持此操作" or str(e) == "此订单号不存在":
                self.failed.emit(str(e))
            else:
                logging.error(e, exc_info=True)
                self.failed.emit(str(e))
        else:
            self.finished.emit()

    def stop(self):
        self._running = False
        logging.info("stop cancel order thread")
        self.terminate()


class ModifyOrderThread(QThread):
    failed = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None, broker_obj=None, modified_order=None):
        super(ModifyOrderThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.broker_obj = broker_obj
        self.modified_order = modified_order

    def run(self):
        try:
            logging.info("start modify order thread")
            data = self.broker_obj.modify_order(self.modified_order)
        except Exception as e:
            if str(e) == "此订单不支持此操作" or str(e) == "此订单号不存在":
                self.failed.emit(str(e))
            else:
                logging.error(e, exc_info=True)
                self.failed.emit(str(e))
        else:
            self.finished.emit()

    def stop(self):
        self._running = False
        logging.info("stop modify order thread")
        self.terminate()


class Sync2DBThread(QThread):

    failed = pyqtSignal()

    def __init__(self, parent=None, aurora_account=None, broker_list=[], db_list=None):
        super(Sync2DBThread, self).__init__(parent)
        self._mutex = QMutex()
        self._running = True
        self.aurora_account = aurora_account
        self.broker_list = broker_list
        self.db_list = db_list

    def run(self):
        error_counter = 0
        while error_counter < 5:
            for broker_obj in self.broker_list:
                try:
                    logging.info("start sync order thread")
                    logging.info(broker_obj.account_number)
                    # jimmy 降低 futu 请求频率, 否则 get_today_orders 与 get_today_deals 间隔太短报错
                    time.sleep(4)
                    acc_orders = broker_obj.get_today_orders()
                    time.sleep(4)
                    acc_deals = broker_obj.get_today_deals()
                    self.sync_to_db(str(broker_obj), acc_orders, acc_deals)
                except Exception as e:
                    logging.error(str(error_counter))
                    logging.error(e, exc_info=True)
                    error_counter += 1
                    time.sleep(1)
            time.sleep(10)
        self.failed.emit()

    def stop(self):
        self._running = False
        logging.info("stop sync order thread")
        self.terminate()

    def sync_to_db(self, broker_str, acc_orders, acc_deals):
        self.db_obj = AuroraDB(self.db_list)
        if acc_orders.shape[0] == 0:
            pass
        else:
            order_db = acc_orders.loc[
                :,
                [
                    "code",
                    "trd_side",
                    "price",
                    "qty",
                    "order_type",
                    "order_status",
                    "create_time",
                ],
            ]

            order_db.rename(
                columns={
                    "trd_side": "side",
                    "order_type": "type",
                    "order_status": "status",
                },
                inplace=True,
            )
            order_db.reset_index(drop=True, inplace=True)
            order_db.loc[:, "username"] = self.aurora_account.username
            order_db.loc[:, "account"] = broker_str
            # 时区转换, 将上传时间统一为北京时间
            order_db.loc[:, "datetime"] = datetime.now(
                timezone("Asia/Shanghai")
            ).strftime("%Y-%m-%d %H:%M:%S")

            # order_db["date"] = datetime.today().date()
            # order_db["time"] = datetime.today().time()
            self.db_obj.insert_order(order_db)

        if acc_deals.shape[0] == 0:
            pass
        else:
            deal_db = acc_deals.loc[
                :, ["code", "trd_side", "price", "qty", "create_time"]
            ]
            deal_db.rename(
                columns={"trd_side": "side", "order_type": "type"},
                inplace=True,
            )
            deal_db.reset_index(drop=True, inplace=True)
            deal_db.loc[:, "username"] = self.aurora_account.username
            deal_db.loc[:, "account"] = broker_str
            # deal_db["date"] = datetime.today().date()
            # deal_db["time"] = datetime.today().time()
            deal_db.loc[:, "datetime"] = datetime.now(
                timezone("Asia/Shanghai")
            ).strftime("%Y-%m-%d %H:%M:%S")

            self.db_obj.insert_deal(deal_db)
