# from charset_normalizer import CharsetMatches
import requests
from account.base import BrokerBase
import os
import os.path
import sys
import time
import pandas as pd

# from urllib import parse
# from shutil import which as By
from .td_url import *
import configparser
from datetime import datetime, timedelta
from datetime import timezone as tz


class TDAcc(BrokerBase):
    def __init__(
        self,
        broker=None,
        account_number=None,
        trading_password=None,
        refresh_token=None,
        client_id=None,
        redirect_uri=None,
    ):
        super(TDAcc, self).__init__(
            broker=broker,
            account_number=account_number,
            trading_password=trading_password,
        )
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        # self.get_local_token()
        self.session = TDAccSession(self.refresh_token, self.client_id)

    def authenticate(self):
        #TODO: implement authentication via self._request()
        if self.account_number:
            return "OK", ""
        else:
            return "Error", "验证失败"

    def _request(self, url, method="GET", params=None, *args, **kwargs):
        resp = self.session.request(method, url, params=params, *args, **kwargs)
        return resp

    def get_local_token(self):
        if not self.refresh_token:
            config = configparser.ConfigParser()
            config.read(r"temp/token.ini")

    # def get_refresh_token(self):
    #     from selenium import webdriver
    #     from selenium.webdriver.chrome.service import Service
    #     from webdriver_manager.chrome import ChromeDriverManager
    #
    #     client_id = self.client_id + "@AMER.OAUTHAP"
    #     url = (
    #         "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri="
    #         + parse.quote(self.redirect_uri)
    #         + "&client_id="
    #         + parse.quote(client_id)
    #     )
    #
    #     options = webdriver.ChromeOptions()
    #     driver = webdriver.Chrome(
    #         service=Service(ChromeDriverManager().install()), options=options
    #     )
    #
    #     driver.get(url)
    #
    #     input("after giving access, hit enter to continue")
    #     code = parse.unquote(driver.current_url.split("code=")[1])
    #
    #     driver.close()
    #
    #     resp = requests.post(
    #         "https://api.tdameritrade.com/v1/oauth2/token",
    #         headers={"Content-Type": "application/x-www-form-urlencoded"},
    #         data={
    #             "grant_type": "authorization_code",
    #             "refresh_token": "",
    #             "access_type": "offline",
    #             "code": code,
    #             "client_id": client_id,
    #             "redirect_uri": self.redirect_uri,
    #         },
    #     )
    #     if resp.status_code != 200:
    #         raise Exception("Could not authenticate!")
    #     return resp.json()

    def place_order(self, order_info_dict):

        # jimmy

        order_kargs = self.parse_order_info(order_info_dict)

        if order_kargs:
            resp = self._request(
                method="POST",
                url=PLACE_ORDER.format(accountId=self.account_number),
                json=order_kargs,
            )

            order_df = pd.DataFrame([order_kargs])

            if resp.status_code == 201:
                return "OK", order_df

            else:
                return (
                    "Error",
                    resp.json(),
                )  # {'error': 'LIMIT order may not have a stop price.'}

        else:
            return "Error", "不支持该订单类型"

    # jimmy
    def parse_order_info(self, order_info_dict):

        price = order_info_dict["price"]
        qty = int(order_info_dict["quantity"])
        code = order_info_dict["symbol"].split(".")[1]
        trd_side = order_info_dict["side"]

        stop_price = order_info_dict["stop price"]
        # limit order 没有止损，如何处理stop price

        # modify order 不支持其他类型
        order_type = "LIMIT"
        time_in_force = "DAY"

        if order_info_dict["price type"] == "Limit":
            order_type = "LIMIT"
        elif order_info_dict["price type"] == "Market":
            order_type = "MARKET"
        elif order_info_dict["price type"] == "Stop Limit":
            order_type = "STOP_LIMIT"
        elif order_info_dict["price type"] == "Stop":
            order_type = "STOP"
        if order_info_dict["time in force"] == "DAY":
            time_in_force = "DAY"
        elif order_info_dict["time in force"] == "GTC":
            time_in_force = "GOOD_TILL_CANCEL"

        if order_type == "LIMIT":
            kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "price": price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }
            return kargs

        elif order_type == "MARKET":
            kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }
            return kargs

        elif order_type == "STOP":
            kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "stopPrice": stop_price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }
            return kargs

        elif order_type == "STOP LIMIT":
            kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "price": price,
                "stopPrice": stop_price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }
            return kargs

    def cancel_order(self, order_id):
        resp = self._request(
            method="DELETE",
            url=CANCEL_ORDER.format(accountId=self.account_number, orderId=order_id),
        )
        if resp.status_code == 200:
            return "已撤单"

        elif resp.status_code == 400:
            raise Exception("无法撤销该订单")  # {} dict

        else:
            raise Exception(resp.json())

    def modify_order(self, modified_order_dict):

        order_id = modified_order_dict["order_id"]
        order_kargs = {}

        code = modified_order_dict["code"]
        order_type = modified_order_dict["order_type"]
        qty = modified_order_dict["qty"]
        price = modified_order_dict["price"]
        trd_side = modified_order_dict["side"]
        stop_price = modified_order_dict["aux_price"]
        time_in_force = "DAY"

        if order_type == "LIMIT":
            order_kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "price": price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }

        elif order_type == "STOP":
            order_kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "stopPrice": stop_price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }

        if order_type == "STOP LIMIT":
            order_kargs = {
                "orderType": order_type,
                "session": "NORMAL",
                "price": price,
                "stopPrice": stop_price,
                "duration": time_in_force,
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": trd_side,
                        "quantity": qty,
                        "instrument": {"symbol": code, "assetType": "EQUITY"},
                    }
                ],
            }

        if order_kargs:
            resp = self._request(
                method="PUT",
                url=REPLACE_ORDER.format(
                    accountId=self.account_number, orderId=order_id
                ),
                json=order_kargs,
            )
            if resp.status_code == 201:
                return "已修改"

            else:
                raise Exception(
                    resp.json()
                )  # {'error': 'LIMIT order may not have a stop price.'}

        else:
            raise Exception("不支持该订单类型")

    def get_acc_asset(self):
        resp = self._request(GET_ACCOUNT.format(accountId=self.account_number))

        if resp.status_code != 200:
            raise Exception("Error Get Account Assets TD")
        else:
            cash = resp.json()["securitiesAccount"]["currentBalances"]["cashBalance"]
            total = resp.json()["securitiesAccount"]["currentBalances"][
                "liquidationValue"
            ]
            market_val = resp.json()["securitiesAccount"]["currentBalances"][
                "longMarketValue"
            ]
            self.total_assets = round(total, 4)
            self.cash = round(cash, 4)
            self.market_val = round(market_val, 4)

            return True

    def get_acc_pos(self):

        resp = self._request(
            method="GET",
            url=GET_ACCOUNT.format(accountId=self.account_number),
            params={"fields": "positions"},
        )

        if resp.status_code != 200:
            raise Exception("Error Get TD Account Positions")

        else:
            content = resp.json()
            if "positions" in content["securitiesAccount"]:
                position_data = content["securitiesAccount"]["positions"]

                for data in position_data:
                    # data["account"] = self.account_number
                    data["account"] = str(self)
                    data["code"] = data["instrument"]["symbol"]
                    data["qty"] = None
                    data["can_sell_qty"] = 0
                    data["cost_price"] = data["averagePrice"]
                    data["position_side"] = "Long"
                    data["nominal_price"] = None
                    data["today_pl_val"] = data["currentDayProfitLoss"]
                    data["pl_val"] = None

                    # jimmy TD 虽然不提供，但也加上
                    data["today_buy_qty"] = "NAN"
                    data["today_sell_qty"] = "NAN"
                    data["today_total_qty"] = "NAN"

                    if data["longQuantity"] != 0:
                        data["qty"] = data["longQuantity"]
                        data["position_side"] = "Long"
                        data["can_sell_qty"] = data["longQuantity"]
                        data["nominal_price"] = (
                            data["marketValue"] / data["longQuantity"]
                        )
                        data["pl_val"] = (
                            data["marketValue"]
                            - data["averagePrice"] * data["longQuantity"]
                        )
                    else:
                        data["qty"] = data["shortQuantity"]
                        data["position_side"] = "Short"
                        data["nominal_price"] = (
                            data["marketValue"] / data["shortQuantity"]
                        )
                        data["pl_val"] = (
                            data["averagePrice"] * data["shortQuantity"]
                            - data["marketValue"]
                        )

                    data.pop("instrument")

                position_pd = pd.json_normalize(position_data)

                self.position = position_pd[
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
                        "today_buy_qty",
                        "today_sell_qty",
                        "today_total_qty",
                    ]
                )

    def get_today_orders(self, fromEnteredTime=None, toEnteredTime=None, status=None):

        resp = self._request(
            url=GET_ORDER_BY_QUERY,
            params={
                "accountId": str(self.account_number),
                "fromEnteredTime": fromEnteredTime,
                "toEnteredTime": toEnteredTime,
                "status": status,
            },
        )

        if resp.status_code == 200:
            content = resp.json()
            if content:
                for data in content:
                    if "stopPrice" not in data:
                        data["aux_price"] = "NAN"
                    if "price" not in data:
                        data["price"] = "NAN"
                    if "closeTime" not in data:
                        data["closeTime"] = "NAN"
                    if "dealt_avg_price" not in data:
                        data["dealt_avg_price"] = "NAN"

                    code = data["orderLegCollection"][0]["instrument"]["symbol"]
                    trade_side = data["orderLegCollection"][0]["instruction"]

                    data["code"] = code
                    data["trd_side"] = trade_side

                    data["order_type"] = data["orderType"]
                    data["qty"] = data["quantity"]
                    data["dealt_qty"] = data["filledQuantity"]
                    data["order_status"] = data["status"]
                    if data["order_status"] == "WORKING":
                        data["order_status"] = "SUBMITTED"
                    if data["order_status"] == "CANCELED":
                        data["order_status"] = "CANCELED_ALL"
                    if data["order_status"] == "FILLED":
                        data["order_status"] = "FILLED_ALL"

                    # data['create_time'] = data['enteredTime']
                    data["create_time"] = data["enteredTime"].replace("T", " ")[:-5]

                    if len(data["create_time"]) == 19:
                        time_array = datetime.strptime(
                            data["create_time"], "%Y-%m-%d %H:%M:%S"
                        )
                        # time_array = time_array + datetime.timedelta(hours=-5)
                        # data['create_time'] = str(time_array)
                        time_array = time_array.replace(tzinfo=tz.utc)
                        time_array = time_array.astimezone(tz(timedelta(hours=-5)))
                        time_array = str(time_array)[:-6]
                        data["create_time"] = time_array

                    data["order_id"] = data["orderId"]

                    if "orderLegCollection" in data:
                        data.pop("orderLegCollection")

                content_pd = pd.json_normalize(content)
                return content_pd[
                    [
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
                ].sort_values(
                    by="create_time", ascending=False
                )  # Dataframe
            else:
                # 没有订单，返回空 Dataframe
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

        else:
            raise Exception(resp.json())

    def get_active_orders(self):
        return self.get_today_orders(status="WORKING")

    def get_history_orders(self, dfrom, dto):
        return self.get_today_orders(fromEnteredTime=dfrom, toEnteredTime=dto)

    def get_today_deals(
        self, fromEnteredTime=None, toEnteredTime=None, status="FILLED"
    ):

        resp = self._request(
            url=GET_ORDER_BY_QUERY,
            params={
                "accountId": str(self.account_number),
                "fromEnteredTime": fromEnteredTime,
                "toEnteredTime": toEnteredTime,
                "status": status,
            },
        )

        if resp.status_code == 200:
            content = resp.json()
            if content:
                for data in content:
                    data["code"] = data["orderLegCollection"][0]["instrument"]["symbol"]
                    data["trd_side"] = data["orderLegCollection"][0]["instruction"]
                    data["price"] = data["orderActivityCollection"][0]["executionLegs"][
                        0
                    ]["price"]
                    data["qty"] = data["orderActivityCollection"][0]["executionLegs"][
                        0
                    ]["quantity"]
                    # exe_time = data['orderActivityCollection'][0]['executionLegs'][0]['time']
                    data["create_time"] = data["orderActivityCollection"][0][
                        "executionLegs"
                    ][0]["time"].replace("T", " ")[:-5]
                    if len(data["create_time"]) == 19:
                        time_array = datetime.strptime(
                            data["create_time"], "%Y-%m-%d %H:%M:%S"
                        )
                        # time_array = time_array + datetime.timedelta(hours=-5)
                        time_array = time_array.replace(tzinfo=tz.utc)
                        time_array = time_array.astimezone(tz(timedelta(hours=-5)))
                        time_array = str(time_array)[:-6]
                        data["create_time"] = time_array

                    # data['create_time'] = data['enteredTime']
                    data["order_id"] = data["orderId"]

                    if "orderLegCollection" in data:
                        data.pop("orderLegCollection")

                    if "orderActivityCollection" in data:
                        data.pop("orderActivityCollection")

                    # data['code'] = code
                    # data['trd_side'] = trade_side
                    # data['price'] = exe_price
                    # data['qty'] = exe_qty

                content_pd = pd.json_normalize(content)
                return content_pd[
                    [
                        "code",
                        "trd_side",
                        "price",
                        "qty",
                        "create_time",
                        "status",
                        "order_id",
                    ]
                ].sort_values(
                    by="create_time", ascending=False
                )  # Dataframe

            else:
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

        else:
            raise Exception(resp.json())

    def get_history_deals(self, dfrom, dto):
        return self.get_today_deals(
            fromEnteredTime=dfrom, toEnteredTime=dto, status="FILLED"
        )

    def get_acc_list(self):
        ret = {}
        resp = self._request(GET_ACCOUNTS)
        for account in resp.json():
            ret[account["securitiesAccount"]["accountId"]] = account
        account_dataframes = []
        for accountId, value in ret.items():
            account_dataframes.append(pd.json_normalize(value))
            account_dataframes[-1].columns = [
                c.replace("securitiesAccount.", "")
                for c in account_dataframes[-1].columns
            ]
        return "OK", pd.concat(account_dataframes)

    # def authenticate(self):
    #
    #     return "OK", ""


class TDAccSession(requests.Session):
    def __init__(self, refresh_token=None, client_id=None):
        super().__init__()
        self._refreshToken = {"token": refresh_token}
        self._accessToken = {
            "token": "",
            "created_at": time.time(),
            "expires_in": -1,
        }  # Set to -1 so that it gets refreshed immediately and its age tracked.
        self._client_id = client_id
        self._headers = {}

    def _set_header_auth(self):
        self._headers.update({"Authorization": "Bearer " + self._accessToken["token"]})

    def request(self, *args, **kwargs):
        self._refresh_token_if_invalid()
        return super().request(headers=self._headers, *args, **kwargs)

    def _is_token_invalid(self):
        if (
            not self._accessToken["token"]
            or self._access_token_age_secs() >= self._accessToken["expires_in"] - 60
        ):
            return True
        else:
            return False

    def _refresh_token_if_invalid(self):
        # Expire the token one minute before its expiration time to be safe
        if self._is_token_invalid():
            token = self.get_access_token(self._refreshToken["token"], self._client_id)
            self._set_access_token(token)

    def _set_access_token(self, token):
        self._accessToken["token"] = token["access_token"]
        self._accessToken["created_at"] = time.time()
        self._accessToken["expires_in"] = token["expires_in"]
        self._set_header_auth()

    def _access_token_age_secs(self):
        return time.time() - self._accessToken["created_at"]

    def get_access_token(self, refresh_token, client_id):
        resp = requests.post(
            "https://api.tdameritrade.com/v1/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_id,
            },
        )
        if resp.status_code != 200:
            raise Exception("Could not authenticate!")
        return resp.json()


def get_accountID(access_token):
    headers = {"Authorization": "Bearer {}".format(access_token)}
    endpoint = r"https://api.tdameritrade.com/v1/accounts"
    content = requests.get(url=endpoint, headers=headers)
    data = content.json()
    print(data)
    account_id = data[0]["securitiesAccount"]["accountId"]
    print(account_id)
    return account_id


# def authenticate(client_id, redirect_uri):
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service
#     from webdriver_manager.chrome import ChromeDriverManager
#
#     client_id = client_id + "@AMER.OAUTHAP"
#     url = (
#         "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri="
#         + parse.quote(redirect_uri)
#         + "&client_id="
#         + parse.quote(client_id)
#     )
#
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()), options=options
#     )
#
#     driver.get(url)
#
#     input("after giving access, hit enter to continue")
#     code = parse.unquote(driver.current_url.split("code=")[1])
#
#     driver.close()
#
#     resp = requests.post(
#         "https://api.tdameritrade.com/v1/oauth2/token",
#         headers={"Content-Type": "application/x-www-form-urlencoded"},
#         data={
#             "grant_type": "authorization_code",
#             "refresh_token": "",
#             "access_type": "offline",
#             "code": code,
#             "client_id": client_id,
#             "redirect_uri": redirect_uri,
#         },
#     )
#     if resp.status_code != 200:
#         raise Exception("Could not authenticate!")
#     return resp.json()


def access_token(refresh_token, client_id):
    resp = requests.post(
        "https://api.tdameritrade.com/v1/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
        },
    )
    if resp.status_code != 200:
        raise Exception("Could not authenticate!")
    print(resp.json())
    return resp.json()


def get_quote():
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/quotes".format("GOOG")
    print(endpoint)
    payload = {
        "apikey": "QGA9OVULNR1HOEOH2WULWUWGCOFJKROS",
    }
    content = requests.get(url=endpoint, params=payload)
    data = content.json()
    print(data)


if __name__ == "__main__":
    # print(authentication(client_id='QGA9OVULNR1HOEOH2WULWUWGCOFJKROS', redirect_uri='http://localhost'))
    # access_token("BCKxdrSBr7JJTnGk3vNeNme/09kDUq5CN6BcM9O3L3rak3e7A25cqpHnYGjtK4Fw1cY44FEsFi36DXuPS0zIQz5Tsi1WemKEkF6btBf/Ik1G75eau4EqrC8iQbz1e0wVd57aWJMayBcznDLyr7sEZ94ONdlMT4DluWrELUZqVQPig34Mzmm/NMBo0Fvirl4wYKUmqpEOr2RbM6VtNIYVeeHWYTLn0fJozJU6KgcXmTYZxhUTX8itDv6fbnvVhCkKnNw/d4tvg42qAtT8DTsTfSlJeUeUW+HcMXI9WBBITOrcuyrqsSoRWH/8+wXQjhnbOt5/sc2TqBeMg3ae856hwzHZO93Xq/ky5jL6Yk6MW2A5tJm/qR27VtxwqiY6J14oXJW0rNyOtCOkH754E7pCMtZ6n6aqg4d7GhPyTh/O2wJKvatOjmROxjxpNsU100MQuG4LYrgoVi/JHHvliX0zLdRKdIHvL1wbnHdMPIzCvdyxLrtZWVpUSdYD7LPIImxLMazHycwvdeKIUXlYKFmigvqNiqjkTe5vWNrQlkMUjrE8OnLBIpUZCIuvyBaEviJbfZ/WJI7hrk3MT7B1+NoMibl+P3wNuunuoHDjc2m5Ju7FiZVPliBWmCqr+liI1AWOkoOXbrU8NMUlMEedYYmGzNRnC39EyKEyRW5JgPGeRkSu6+HB1eGAzcoJ3uXo88lYupyAA+BaI2EvvZy8zc3NQResnojq4jull55TIxXpOv04vji84PuLGURtKn3qiwGtqB8P3kDqKJC93S/Eh9zvMQMEETIipgG0itPrBSNRFqnQPZzLIroTO7CfIUehTYlmhETIbZXzT+E1wyYKcanrg/na1jmyg+hFcOPqE1TkyRu+vZ+8kAe46KhlUoW1A4SFL8ytn85AR3E=212FD3x19z9sWBHDJACbC00B75E",client_id = "QGA9OVULNR1HOEOH2WULWUWGCOFJKROS")
    get_accountID(
        "P3hNcGY2RfqgjR6NiqdUS9LBGBUHl6vaFiwp2WTTJrW/Iamyj0ZEnB1tA0alP1ZtqG0gCYckNSDtvEAF3jNuDBaqmM1+M0aBWMqbznI8/MgsBJCDzPep20L2gcHdSd5XygZObAgRq0BMgwM3UzmC9oAJhZ4ElRS/iKczVagmEG4qYXzbDs0somx4XfrjHPCLwph2/mS7hva40rZ+e5P0rU2Q4GYB45XD/w4nP6b5vmZgA5IxTYKzVPQruDiWwF6v1eQPDOJ8TuFu8k8XgOlQ28GPQjDPQmalKhW7O8vYR3OXq9/YUBL0XUogG/GK0BAMHAOOkhPbIvOCaGd0CX+TXHFgxzdROmI7YRYNFCxuPWYHU0QMfSgDgKflM90V1N3mgSTKZZkALLqNYu0fex+GjW8g2V3T1djmAUh34vUsU7GLEKjfY+cwnMVYU82XXbzAVAgdF6xTiekN9GZDAxOGYjc05cJVPWcTmqPLfoHpVqis4jKjuSjuxIGuyOF5ODqNRPTQYc4x0D6Aht8UjBSbDQidBL+rKOPEUi+oSis16vLpwqZpM100MQuG4LYrgoVi/JHHvlD+PHmk20Dn3CHPHIRk/LYJi5gpQWr1L9Sb6a//GZZOlOeTHbMltAcLbYO4jWkSHC3y8goM6VMxjwYHB1WgXY1JBzmB+U59hfrhihhwZKEf3q08YDqnCwwpgKWL1fl0Q/m7TP+nj4qoJRU048f2QKZzQkzLfW9dui57Zu0qOJQE/WJaw4VYcGyo0oqJbkVX97obuhUzaBX6uptgQnwWudXTjRDlhqB6I0V3KzpRTILQq6oHPqhETu01UwDOHNX7ZlLzf+0vlqg9JEXSY25vjle4+E7luyTbihJwfjt1CLbIe0SSvw0g6OL4+yl/sEpv+QQDEtfUUgdG2lsS8n4TVyNgL/iiT3WsL0xlCAejgi4nBq7PJ1oQccSm81+XbBFtLaBfT7htNdNEJWwrcYzQHiu1VnZCXrnZalsfLXXL2jrzNDR1GK/AX+zXhjl+i1Gdjp4rhlmZgMiGSXE1NytTC9buVZI5U7+8feJIpongs8C7LNoqAlaKGZ8ho9ZycXJGyWPEZctpUmeAL4CM6YXKgpdlyPKrWA+3UwV5uIm46R1ZjuLuGg==212FD3x19z9sWBHDJACbC00B75E"
    )
