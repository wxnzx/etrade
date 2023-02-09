from PyQt5.QtCore import QObject
import pandas as pd


class AuroraAccount(object):
    broker_accounts = []

    def __init__(
        self,
        username=None,
        password=None,
    ):
        self.username = username
        self.password = password
        self.account_tier = "standard"
        self.logged_in = False
        self.unlock = False
        # self.broker_accounts = list()


class BrokerBase(QObject):
    def __init__(
        self,
        broker=None,
        username=None,
        password=None,
        account_number=None,
        trading_password=None,
    ):
        super(BrokerBase, self).__init__()
        self.broker = broker
        self.username = username
        self.password = password
        self.account_number = account_number
        self.trading_password = trading_password
        # self.order_columns = [
        #     "Account",
        #     "Code",
        #     "Side",
        #     "Order Type",
        #     "Price",
        #     "Qty",
        #     "Dealt Qty",
        #     "Dealt Avg Price",
        #     "Order Status",
        #     "Create Time",
        #     "Aux Price",
        #     "Order Id",
        # ]
        self.total_assets = float()
        self.cash = float()
        self.market_val = float()
        self.position = pd.DataFrame(
            columns=[
                "account",
                "code",
                "qty",
                "can_sell_qty",
                "nominal_price",
                "cost_price",
                "position_side",
                "today_pl_val",
                "pl_val",
                # 后三项不管券商有没有先都加上
                "today_buy_qty",
                "today_sell_qty",
                "today_total_qty",
            ]
        )

    def authenticate(self, *args, **kwargs):
        ...

    def get_acc_asset(self, *args, **kwargs):
        ...

    def get_acc_list(self, *args, **kwargs):
        ...

    def get_acc_pos(self, *args, **kwargs):
        ...

    def get_today_orders(self, *args, **kwargs):
        ...

    def get_history_orders(self, *args, **kwargs):
        ...

    def get_active_orders(self, *args, **kwargs):
        ...

    def get_today_deals(self, *args, **kwargs):
        ...

    def get_history_deals(self, *args, **kwargs):
        ...

    def place_order(self, *args, **kwargs):
        """If successfully placed an order, returns OK, pd.DataFrame()"""
        ...

    def cancel_order(self, *args, **kwargs):
        ...

    def modify_order(self, *args, **kwargs):
        ...

    def __repr__(self):
        return str(self.broker) + "-" + str(self.account_number)

