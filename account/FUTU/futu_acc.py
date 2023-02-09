from ..base import BrokerBase
import logging
import futu
import os
import numpy as np
import socket
from datetime import datetime


class FutuAcc(BrokerBase):
    def __init__(
        self,
        broker=None,
        account_number=None,
        trading_password=None,
        futu_host=None,
        futu_port=None,
    ):
        super(FutuAcc, self).__init__(
            broker=broker,
            account_number=account_number,
            trading_password=trading_password,
        )
        self.futu_host = futu_host
        self.futu_port = futu_port
        self.market = futu.TrdMarket.US
        self.get_security_firm()
        self.get_trading_env()

        logging.info(self.security_firm)
        logging.info(self.futu_env)

    def get_security_firm(self):
        if self.broker == "FUTUBULL 富途牛牛":
            self.security_firm = futu.SecurityFirm.FUTUSECURITIES
        elif self.broker == "FUTU MOOMOO":
            self.security_firm = futu.SecurityFirm.FUTUINC
        else:
            self.security_firm = None

    def get_trading_env(self):
        if os.environ.get("FUTU_ENV") == "REAL":
            self.futu_env = futu.TrdEnv.REAL
        elif os.environ.get("FUTU_ENV") == "SIMULATE":
            self.futu_env = futu.TrdEnv.SIMULATE

    def get_acc_list(self):
        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.get_acc_list()
        trd_ctx.close()
        if ret == futu.RET_OK:
            logging.info(data)
            if self.futu_env == futu.TrdEnv.SIMULATE:
                self.acc_df = data.loc[
                    (data["trd_env"] == "SIMULATE") & (data["sim_acc_type"] == "STOCK")
                ]
            elif self.futu_env == futu.TrdEnv.REAL:
                self.acc_df = data.loc[
                    (data["trd_env"] == "REAL")
                    # & (data["sim_acc_type"] == "STOCK")
                ]
            else:
                return "Error", "没有可用的交易账户"
            return "OK", self.acc_df
        else:
            return "Error", "无法获取账户"

    def get_quote(self, code_list):
        quote_ctx = futu.OpenQuoteContext(host=self.futu_host, port=self.futu_port)
        ret_sub, err_message = quote_ctx.subscribe(
            code_list, [futu.SubType.QUOTE], subscribe_push=False
        )
        if ret_sub == futu.RET_OK:  # Subscription successful
            ret, data = quote_ctx.get_stock_quote(
                code_list
            )  # Get real-time data of subscription stock quotes
            quote_ctx.close()
            if ret == futu.RET_OK:
                return (
                    "OK",
                    data[
                        [
                            "code",
                            "data_time",
                            "last_price",
                            "open_price",
                            "high_price",
                            "low_price",
                            "prev_close_price",
                            "volume",
                            "turnover",
                        ]
                    ],
                )
            else:
                return "Error", data
        else:
            quote_ctx.close()
            return "Error", err_message

    def get_acc_asset(self):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.accinfo_query(
            acc_id=int(self.account_number),
            trd_env=self.futu_env,
            refresh_cache=True,
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            self.total_assets = round(data["total_assets"][0], 3)
            self.cash = round(data["cash"][0], 3)
            self.market_val = round(data["market_val"][0], 3)
            return True
        else:
            raise Exception("Error Get Account Assets")

    def get_acc_pos(self):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.position_list_query(
            trd_env=self.futu_env, acc_id=int(self.account_number)
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            # data["today_buy_qty"] = data["today_buy_qty"].apply(lambda x: str(x))
            # data["today_sell_qty"] = data["today_sell_qty"].apply(lambda x: str(x))
            # data.loc[
            #     data["today_buy_qty"].str.contains("N/A"), ["today_buy_qty"]
            # ] = None
            # data.loc[
            #     data["today_sell_qty"].str.contains("N/A"), ["today_sell_qty"]
            # ] = None
            data["today_buy_qty"] = data["today_buy_qty"].apply(
                lambda x: np.nan if "N/A" in str(x) else int(x)
            )
            data["today_sell_qty"] = data["today_sell_qty"].apply(
                lambda x: np.nan if "N/A" in str(x) else int(x)
            )
            data["today_total_qty"] = data["today_buy_qty"] + data["today_sell_qty"]
            # data["unrealized_pl"] = data["unrealized_pl"].apply(
            #     lambda x: np.nan if "N/A" in str(x) else float(x)
            # )
            # data["realized_pl"] = data["realized_pl"].apply(
            #     lambda x: np.nan if "N/A" in str(x) else float(x)
            # )

            data.insert(0, column="account", value=str(self))

            self.position = data[
                [
                    "account",
                    "code",
                    "qty",
                    "can_sell_qty",
                    "nominal_price",
                    "cost_price",
                    "position_side",
                    "today_pl_val",
                    "pl_val",
                    "today_buy_qty",
                    "today_sell_qty",
                    "today_total_qty",
                ]
            ].round(3)
            return True
        else:
            raise Exception("Failed to get Position list")

    def get_today_orders(self):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.order_list_query(
            trd_env=self.futu_env, acc_id=int(self.account_number)
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            data.loc[
                data["order_type"] == futu.OrderType.NORMAL, "order_type"
            ] = "LIMIT"
            data.loc[data["fill_outside_rth"] == True, "fill_outside_rth"] = "EXTENDED"
            data.loc[data["fill_outside_rth"] == False, "fill_outside_rth"] = "REGULAR"
            data.rename(columns={"fill_outside_rth": "market_session"}, inplace=True)
            data["create_time"] = data["create_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            )
            return data[
                [
                    "code",
                    "trd_side",
                    "order_type",
                    "price",
                    "qty",
                    "dealt_qty",
                    "dealt_avg_price",
                    "order_status",
                    "time_in_force",
                    "market_session",
                    "create_time",
                    "aux_price",
                    "order_id",
                ]
            ].sort_values(by="create_time", ascending=False)
        else:
            print("acc details error: ", data)
            raise Exception("Failed to get order information")

    def get_active_orders(self):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.order_list_query(
            trd_env=self.futu_env, acc_id=int(self.account_number)
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            open_order_status = [
                "NONE",
                "WAITING_SUBMIT",
                "SUBMITTING",
                "SUBMITTED",
                "FILLED_PART",
            ]
            data = data.loc[data["order_status"].isin(open_order_status)]
            data.loc[
                data["order_type"] == futu.OrderType.NORMAL, "order_type"
            ] = "LIMIT"
            data.loc[data["fill_outside_rth"] == True, "fill_outside_rth"] = "EXTENDED"
            data.loc[data["fill_outside_rth"] == False, "fill_outside_rth"] = "REGULAR"
            data.rename(columns={"fill_outside_rth": "market_session"}, inplace=True)
            data["create_time"] = data["create_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            )
            return data[
                [
                    "code",
                    "trd_side",
                    "order_type",
                    "price",
                    "qty",
                    "dealt_qty",
                    "dealt_avg_price",
                    "order_status",
                    "time_in_force",
                    "market_session",
                    "create_time",
                    "aux_price",
                    "order_id",
                ]
            ].sort_values(by="create_time", ascending=False)
        else:
            print("acc details error: ", data)
            raise Exception("Failed to get order information")

    def get_history_orders(self, dfrom, dto):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.history_order_list_query(
            start=dfrom, end=dto, trd_env=self.futu_env, acc_id=int(self.account_number)
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            data.loc[
                data["order_type"] == futu.OrderType.NORMAL, "order_type"
            ] = "LIMIT"
            data.loc[data["fill_outside_rth"] == True, "fill_outside_rth"] = "EXTENDED"
            data.loc[data["fill_outside_rth"] == False, "fill_outside_rth"] = "REGULAR"
            data.rename(columns={"fill_outside_rth": "market_session"}, inplace=True)
            data["create_time"] = data["create_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            )
            return data[
                [
                    "code",
                    "trd_side",
                    "order_type",
                    "price",
                    "qty",
                    "dealt_qty",
                    "dealt_avg_price",
                    "order_status",
                    "time_in_force",
                    "market_session",
                    "create_time",
                    "aux_price",
                    "order_id",
                ]
            ].sort_values(by="create_time", ascending=False)
        else:
            print("acc details error: ", data)
            raise Exception("Failed to get order information")

    def get_today_deals(self):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.deal_list_query(
            trd_env=futu.TrdEnv.REAL, acc_id=int(self.account_number)
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            data["create_time"] = data["create_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            )
            return data[
                [
                    "code",
                    "trd_side",
                    "price",
                    "qty",
                    "create_time",
                    "status",
                    "order_id",
                ]
            ].sort_values(by="create_time", ascending=False)
        else:
            print("acc details error: ", data)
            raise Exception("Failed to get DEAL information")

    def get_history_deals(self, dfrom, dto):

        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.history_deal_list_query(
            start=dfrom,
            end=dto,
            trd_env=futu.TrdEnv.REAL,
            acc_id=int(self.account_number),
        )
        trd_ctx.close()
        if ret == futu.RET_OK:
            data["create_time"] = data["create_time"].apply(
                lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
            )
            return data[
                [
                    "code",
                    "trd_side",
                    "price",
                    "qty",
                    "create_time",
                    "status",
                    "order_id",
                ]
            ].sort_values(by="create_time", ascending=False)
        else:
            print("acc details error: ", ret, data)
            raise Exception("Failed to get order information")

    def place_order(self, order_info_dict):
        kargs = self.parse_order_info(order_info_dict)
        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.unlock_trade(self.trading_password)
        # CLOSE CONN FIRST!!!!!
        if ret == futu.RET_OK:
            ret, data = trd_ctx.place_order(**kargs)
            trd_ctx.close()
            if ret == futu.RET_OK:
                return "OK", data
            else:
                return "Error", data
        else:
            trd_ctx.close()
            return "UnlockError", data

    def parse_order_info(self, order_info_dict):
        price = order_info_dict["price"]
        qty = order_info_dict["quantity"]
        code = order_info_dict["symbol"]
        trd_side = order_info_dict["side"]
        acc_id = int(self.account_number)
        aux_price = order_info_dict["stop price"]
        trd_env = self.futu_env
        # ORDER TYPE
        if order_info_dict["price type"] == "Limit":
            order_type = futu.OrderType.NORMAL
        elif order_info_dict["price type"] == "Market":
            order_type = futu.OrderType.MARKET
        elif order_info_dict["price type"] == "Stop Limit":
            order_type = futu.OrderType.STOP_LIMIT
        elif order_info_dict["price type"] == "Stop":
            order_type = futu.OrderType.STOP
        # TIF
        if order_info_dict["time in force"] == "DAY":
            time_in_force = futu.TimeInForce.DAY
        elif order_info_dict["time in force"] == "GTC":
            time_in_force = futu.TimeInForce.GTC
        # TRADING HOURS
        if order_info_dict["market session"] == "REGULAR":
            market_session = False
        elif order_info_dict["market session"] == "EXTENDED":
            market_session = True
        else:
            market_session = False

        kargs = {
            "price": price,
            "qty": qty,
            "code": code,
            "trd_side": trd_side,
            "order_type": order_type,
            "acc_id": acc_id,
            "time_in_force": time_in_force,
            "aux_price": aux_price,
            "fill_outside_rth": market_session,
            "trd_env": trd_env,
        }
        return kargs

    def cancel_order(self, order_id):
        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.unlock_trade(self.trading_password)
        if ret == futu.RET_OK:
            ret, data = trd_ctx.modify_order(
                futu.ModifyOrderOp.CANCEL, order_id, 0, 0, trd_env=self.futu_env
            )
            if ret == futu.RET_OK:
                trd_ctx.close()
                return data
            else:
                trd_ctx.close()
                raise Exception(str(data))
        else:
            trd_ctx.close()
            raise Exception("UnlockError")

    def modify_order(self, modified_order_dict):
        trd_ctx = futu.OpenSecTradeContext(
            filter_trdmarket=self.market,
            host=self.futu_host,
            port=self.futu_port,
            security_firm=self.security_firm,
        )
        ret, data = trd_ctx.unlock_trade(self.trading_password)
        order_id = modified_order_dict["order id"]
        qty = modified_order_dict["qty"]
        price = modified_order_dict["price"]
        aux_price = modified_order_dict["aux price"]

        if ret == futu.RET_OK:
            ret, data = trd_ctx.modify_order(
                futu.ModifyOrderOp.NORMAL,
                order_id,
                qty,
                price,
                trd_env=self.futu_env,
                aux_price=aux_price,
            )
            if ret == futu.RET_OK:
                trd_ctx.close()
                return data
            else:
                trd_ctx.close()
                raise Exception(str(data))
        else:
            trd_ctx.close()
            raise Exception("UnlockError")

    def authenticate(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.futu_host, self.futu_port))
        sock.close()
        if result == 0:
            # "Port is open"

            trd_ctx = futu.OpenSecTradeContext(
                filter_trdmarket=self.market,
                host=self.futu_host,
                port=self.futu_port,
                security_firm=self.security_firm,
            )
            ret, data = trd_ctx.unlock_trade(self.trading_password)
            trd_ctx.close()
            logging.info(ret)
            if ret != futu.RET_OK:
                logging.warning(f"解锁交易失败: {data}")
                return "Error", data
            elif data != None:
                logging.warning(f"解锁交易:{data}")
                if self.futu_env == futu.TrdEnv.SIMULATE:
                    return "OK", ""
                else:
                    return "Error", data
            else:
                logging.warning(f"解锁交易成功:{data}")
                return "OK", None
        else:
            return "Error", "端口未开启，请打开FutuOpenD"
