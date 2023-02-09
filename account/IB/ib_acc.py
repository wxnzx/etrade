from account.base import BrokerBase
from .ib_session import IBAccSession
from .ib_url import *
import time
import logging
import json
import pandas as pd
import numpy as np
from datetime import datetime, date


formatter = "[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=formatter)


class IBAcc(BrokerBase):
    def __init__(self, broker=None, username=None, password=None, account_number=None):
        super(IBAcc, self).__init__(
            broker=broker,
            username=username,
            password=password,
            account_number=account_number,
        )
        self.session = IBAccSession(username, password)

    def _request(self, url, method="GET", params=None, *args, **kwargs):
        resp = self.session._request(method, url, params=params, *args, **kwargs)
        return resp

    def authenticate(self):
        self.session._reconnect()
        time.sleep(4)
        if self.account_number and self.session._is_authenticated():
            return "OK", ""
        else:
            return "Error", "IB验证失败"

    def get_acc_list(self):
        resp = self._request(method="GET", url=BASE + ISERVER_ACCOUNT)
        if resp.status_code != 200:
            return "Error", str(resp.status_code) + str(resp.text)
        else:
            acc_list = resp.json()["accounts"]
            acc_df = pd.DataFrame(acc_list, columns=["Account ID"])
            return "OK", acc_df

    def search_for_conid(self, ticker):
        payload = {"symbol": ticker}
        resp = self._request(method="GET", url=BASE + SEARCH_CONID, params=payload)
        if resp.status_code == 200:
            return "OK", resp.json()[0]["conid"]
        else:
            return "Error", resp.status_code

    def parse_order_info(self, order_info_dict):
        code = order_info_dict["symbol"].split(".")[1]
        ret, data = self.search_for_conid(code)
        if ret == "OK":
            conid = data
        else:
            raise Exception(str(data))

        qty = order_info_dict["quantity"]
        trd_side = order_info_dict["side"]

        market_session = order_info_dict["market session"]
        if order_info_dict["price type"] == "Limit":
            order_type = "LMT"
            price = order_info_dict["price"]
            aux_price = None
        elif order_info_dict["price type"] == "Market":
            order_type = "MKT"
            price = None
            aux_price = None
        elif order_info_dict["price type"] == "Stop Limit":
            order_type = "STOP_LIMIT"
            price = order_info_dict["price"]
            aux_price = order_info_dict["stop price"]
        elif order_info_dict["price type"] == "Stop":
            order_type = "STP"
            aux_price = None
            price = order_info_dict["stop price"]

        if order_info_dict["time in force"] == "DAY":
            tif = "DAY"
        elif order_info_dict["time in force"] == "GTC":
            tif = "GTC"

        if market_session == "REGULAR":
            outsideRTH = False
        elif market_session == "EXTENDED":
            outsideRTH = True
        payload = {
            "orders": [
                {
                    "acctId": f"{self.account_number}",
                    "conidex": f"{conid}",
                    "orderType": f"{order_type}",
                    "listingExchange": "SMART",
                    "outsideRTH": outsideRTH,
                    "price": price,
                    "auxPrice": aux_price,
                    "side": f"{trd_side}",
                    "ticker": f"{code}",
                    "tif": f"{tif}",
                    "quantity": qty,
                }
            ]
        }
        logging.info(payload)
        return json.dumps(payload)

    def place_order(self, order_info_dict):
        url = BASE + PLACE_ORDER.format(accountID=self.account_number)
        payload = self.parse_order_info(order_info_dict)
        resp = self._request(
            data=payload,
            method="POST",
            url=url,
        )
        if resp.status_code == 200:
            message = resp.json()[0]["message"][0]
            while True:
                if "?" in message or "sure" in message or "Confirm" in message:
                    logging.info(message)
                    message_id = resp.json()[0]["id"]
                    ret, data = self.reply_message(message_id)
                    if ret == "OK":
                        try:
                            message = data[0]["message"][0]
                        except Exception:
                            break
                    else:
                        return "Error", str(ret) + str(data)
                else:
                    break
            return "OK", pd.DataFrame()

        else:
            return "Error", str(resp.status_code) + str(resp.text)

    def reply_message(self, message_id):
        url = BASE + ORDER_REPLY.format(replyid=message_id)
        payload = {"confirmed": True}
        resp = self._request(data=json.dumps(payload), method="POST", url=url)
        if resp.status_code == 200:
            return "OK", resp.json()
        else:
            return resp.status_code, resp.text

    def get_acc_asset(self):
        url = BASE + SUMMARY.format(accountID=self.account_number)
        resp = self._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()
            self.total_assets = round(data["equitywithloanvalue-s"]["amount"], 3)
            self.cash = round(data["totalcashvalue-s"]["amount"], 3)
            self.market_val = round(data["grosspositionvalue-s"]["amount"], 3)
            return True
        else:
            raise Exception("Error Get Account Assets")

    def get_acc_pos(self):
        pageID = 0
        while True:
            url = BASE + POSITIONS.format(accountID=self.account_number, pageID=pageID)
            resp = self._request(method="GET", url=url)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) == 0:
                    break
                else:
                    df = pd.DataFrame(data)
                    df = df[
                        [
                            "contractDesc",
                            "position",
                            "mktPrice",
                            "avgCost",
                            "realizedPnl",
                            "unrealizedPnl",
                        ]
                    ]
                    df.insert(0, column="account", value=str(self))
                    df["code"] = df["contractDesc"]
                    df["qty"] = df["position"]
                    df["can_sell_qty"] = np.NaN
                    df["nominal_price"] = df["mktPrice"]
                    df["cost_price"] = df["avgCost"]
                    df["position_side"] = np.where(df["position"] > 0, "BUY", "SELL")
                    df["today_pl_val"] = np.NaN
                    df["pl_val"] = df["realizedPnl"] + df["unrealizedPnl"]
                    df["today_buy_qty"] = np.NaN
                    df["today_sell_qty"] = np.NaN
                    df["today_total_qty"] = np.NaN
                    pos_df = df[
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
                    ]
                    self.position = (
                        pd.concat([self.position, pos_df])
                        .drop_duplicates(subset="code", keep="last", ignore_index=True)
                        .reset_index(drop=True)
                    )
                    pageID = pageID + 1
            else:
                raise Exception(str(resp.status_code) + str(resp.text))
        return True

    def get_active_orders(self):
        url = BASE + ORDERS
        resp = self._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()["orders"]
            if len(data) == 0:
                return pd.DataFrame(
                    columns=[
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
                )
            df = pd.DataFrame(data)
            open_order_status = ["Submitted", "PreSubmitted"]
            df = df.loc[df["status"].isin(open_order_status)]
            try:
                df["auxPrice"]
            except Exception:
                df["auxPrice"] = np.NaN
            df = df[
                [
                    "ticker",
                    "side",
                    "orderType",
                    "price",
                    "remainingQuantity",
                    "filledQuantity",
                    "status",
                    "timeInForce",
                    "outsideRTH",
                    "lastExecutionTime_r",
                    "auxPrice",
                    "orderId",
                ]
            ]
            df["code"] = df["ticker"]
            df["trd_side"] = df["side"]
            df["order_type"] = df["orderType"]
            df["qty"] = df["remainingQuantity"] + df["filledQuantity"]
            df["dealt_qty"] = df["filledQuantity"]
            df["dealt_avg_price"] = np.NaN
            df["order_status"] = df["status"]
            df["time_in_force"] = df["timeInForce"]
            df.loc[df["outsideRTH"] == True, "market_session"] = "EXTENDED"
            df.loc[df["outsideRTH"] == False, "market_session"] = "REGULAR"
            df["create_time"] = df["lastExecutionTime_r"].apply(
                lambda x: datetime.fromtimestamp(int(x) / 1000)
            )
            df["aux_price"] = df["auxPrice"]
            df["order_id"] = df["orderId"]
            return df[
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

    def get_today_orders(self):
        url = BASE + ORDERS
        resp = self._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()["orders"]
            if len(data) == 0:
                return pd.DataFrame(
                    columns=[
                        "code",
                        "trd_side",
                        "order_type",
                        "price",
                        "qty",
                        "dealt_qty",
                        "dealt_avg_price",
                        "order_status",
                        "create_time",
                        "aux_price",
                        "order_id",
                    ]
                )
            df = pd.DataFrame(data)
            try:
                df["auxPrice"]
            except Exception:
                df["auxPrice"] = np.NaN
            df = df[
                [
                    "ticker",
                    "side",
                    "orderType",
                    "price",
                    "remainingQuantity",
                    "filledQuantity",
                    "status",
                    "timeInForce",
                    "outsideRTH",
                    "lastExecutionTime_r",
                    "auxPrice",
                    "orderId",
                ]
            ]
            df["code"] = df["ticker"]
            df["trd_side"] = df["side"]
            df["order_type"] = df["orderType"]
            df["qty"] = df["remainingQuantity"] + df["filledQuantity"]
            df["dealt_qty"] = df["filledQuantity"]
            df["dealt_avg_price"] = np.NaN
            df["order_status"] = df["status"]
            df["time_in_force"] = df["timeInForce"]
            df.loc[df["outsideRTH"] == True, "market_session"] = "EXTENDED"
            df.loc[df["outsideRTH"] == False, "market_session"] = "REGULAR"
            df["create_time"] = df["lastExecutionTime_r"].apply(
                lambda x: datetime.fromtimestamp(int(x) / 1000)
            )
            df["aux_price"] = df["auxPrice"]
            df["order_id"] = df["orderId"]
            return df[
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

    def get_history_orders(self, *args, **kwargs):
        return pd.DataFrame(
            columns=[
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
        )

    def get_today_deals(self):
        url = BASE + TRADES
        resp = self._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) == 0:
                return pd.DataFrame(
                    columns=[
                        "code",
                        "trd_side",
                        "price",
                        "qty",
                        "create_time",
                        "status",
                        "order_id",
                    ]
                )
            df = pd.DataFrame(data)
            df = df[["symbol", "side", "price", "size", "trade_time_r", "execution_id"]]
            df["code"] = df["symbol"]
            df["trd_side"] = df["side"]
            df["qty"] = df["size"]
            df["create_time"] = df["trade_time_r"].apply(
                lambda x: datetime.fromtimestamp(int(x) / 1000)
            )

            df["status"] = pd.NA
            df["order_id"] = df["execution_id"]
            df["date"] = df["create_time"].apply(lambda x: x.date())
            today = date.today()
            df = df.loc[df["date"] == today]
            return df[
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

    def get_history_deals(self, dfrom, dto):
        url = BASE + TRADES
        resp = self._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) == 0:
                return pd.DataFrame(
                    columns=[
                        "code",
                        "trd_side",
                        "price",
                        "qty",
                        "create_time",
                        "status",
                        "order_id",
                    ]
                )
            df = pd.DataFrame(data)
            df = df[["symbol", "side", "price", "size", "trade_time_r", "execution_id"]]
            df["code"] = df["symbol"]
            df["trd_side"] = df["side"]
            df["qty"] = df["size"]
            df["create_time"] = df["trade_time_r"].apply(
                lambda x: datetime.fromtimestamp(int(x) / 1000)
            )

            df["status"] = pd.NA
            df["order_id"] = df["execution_id"]
            df["date"] = df["create_time"].apply(lambda x: x.date())
            dfrom_date = datetime.strptime(dfrom, "%Y-%m-%d").date()
            dto_date = datetime.strptime(dto, "%Y-%m-%d").date()
            mask = (df["date"] >= dfrom_date) & (df["date"] <= dto_date)
            df = df.loc[mask]
            return df[
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

    def cancel_order(self, order_id):
        url = BASE + CANCEL_ORDER.format(
            accountID=self.account_number, orderID=order_id
        )
        resp = self._request(method="DELETE", url=url)
        if resp.status_code == 200:
            return resp.json()["msg"]
        else:
            raise Exception(str(resp.status_code))

    def modify_order(self, modified_order_dict):
        order_id = modified_order_dict["order id"]
        code = modified_order_dict["code"]
        ret, data = self.search_for_conid(code)
        if ret == "OK":
            conid = data
        else:
            raise Exception(str(data))
        order_type = modified_order_dict["order type"]
        qty = modified_order_dict["qty"]
        price = modified_order_dict["price"]
        trd_side = modified_order_dict["side"]
        aux_price = modified_order_dict["aux price"]
        if modified_order_dict["order type"] == "Limit":
            order_type = "LMT"
            aux_price = None
        elif modified_order_dict["order type"] == "Stop":
            order_type = "STP"
            aux_price = None
        elif modified_order_dict["order type"] == "Stop Limit":
            order_type = "STOP_LIMIT"
        time_in_force = modified_order_dict["time in force"]
        if modified_order_dict["market session"] == "REGULAR":
            market_session = False
        elif modified_order_dict["market session"] == "EXTENDED":
            market_session = True
        payload = {
            "acctId": f"{self.account_number}",
            "conidex": conid,
            "orderType": order_type,
            "outsideRTH": market_session,
            "price": price,
            "auxPrice": aux_price,
            "side": trd_side,
            "tif": time_in_force,
            "quantity": int(qty),
        }
        url = BASE + MODIFY_ORDER.format(
            accountID=self.account_number, orderID=order_id
        )
        resp = self._request(method="POST", url=url, data=json.dumps(payload))
        if resp.status_code == 200:
            logging.info(resp.json())
            try:
                message = resp.json()[0]["message"][0]
            except Exception:
                message = ""
            while True:
                if "?" in message or "sure" in message or "Confirm" in message:
                    logging.info(message)
                    message_id = resp.json()[0]["id"]
                    ret, data = self.reply_message(message_id)
                    if ret == "OK":
                        try:
                            message = data[0]["message"][0]
                        except Exception:
                            break
                    else:
                        raise Exception(str(ret) + str(data))
                else:
                    break
            return "OK"
        else:
            raise Exception(str(resp.status_code) + str(resp.text))


if __name__ == "__main__":
    ib_acc = IBAcc("", "", "")
    # print(ib_acc._is_port_in_use(5000))
    # ib_acc._start_server()
    # res, data = ib_acc._authenticate_gateway()
    # logging.info(res)
    # logging.info(data)
    # ib_acc.place_order("IQ")
    # ib_acc.get_open_orders()
    # logging.info(ib_acc.search_for_conid("BNGO"))
    # logging.info(ib_acc._is_authenticated())
    print(ib_acc.get_active_orders())
