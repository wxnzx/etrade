from account.base import BrokerBase
from .etrade_session import ETradeAccSession
from .etrade_url import *
import time
import logging
import json
import pandas as pd
import numpy as np
import random
import re
import lxml
import xmltodict
from datetime import datetime, date

formatter = "[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)"
logging.basicConfig(level=logging.INFO, format=formatter)


class ETradeAcc(BrokerBase):
    def __init__(self, broker=None, username=None, password=None, account_number=None,
                 consumer_key=None, consumer_secret=None):
        super(ETradeAcc, self).__init__(
            broker=broker,
            username=username,
            password=password,
            account_number=account_number,
        )
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.session = ETradeAccSession(username, password, self.consumer_key, self.consumer_secret).get_session()

    def _request(self, url, method="GET", params=None, headers=None, *args, **kwargs):
        resp = self.session.request(method, url, params=params, headers=headers, *args, **kwargs)
        return resp

    def get_acc_list(self):
        resp = self._request(url=BASE + List_Accounts, header_auth=True)
        if resp.status_code == 200:
            data = resp.json()
            accounts_list = data["AccountListResponse"]["Accounts"]["Account"]
            acc_df = accounts_list[0]["accountId"]
            return "OK", acc_df
        else:
            return "Error", str(resp.status_code) + str(resp.text)

    def authenticate(self):
        if self.account_number and self.get_acc_list():
            return "OK", ""
        else:
            return "Error", "E*Trade验证失败"

    def get_accountIdKey(self):
        resp = self._request(url=BASE + List_Accounts, header_auth=True)
        if resp.status_code != 200:
            return "Error", str(resp.status_code) + str(resp.text)
        else:
            data = resp.json()
            accounts_list = data["AccountListResponse"]["Accounts"]["Account"]
            accountIdKey = accounts_list[0]["accountIdKey"]
            institutionType = accounts_list[0]["institutionType"]
            return accountIdKey, institutionType

    def get_acc_asset(self):
        accountIdKey, institutionType = self.get_accountIdKey()
        url = BASE + balance_asset.format(accountIdKey=accountIdKey)
        params = {"instType": institutionType, "realTimeNAV": "true"}
        headers = {"consumerkey": self.consumer_key}
        resp = self._request(url=url, header_auth=True, params=params, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            self.total_assets = round(data["BalanceResponse"]["Computed"]["RealTimeValues"]["totalAccountValue"], 4)
            self.cash = round(data["BalanceResponse"]["Computed"]["netCash"], 4)
            self.market_val = round(data["BalanceResponse"]["Computed"]["RealTimeValues"]["netMv"], 4)
            return True
        else:
            raise Exception("Error Get Account Assets")

    def get_acc_pos(self):
        accountIdKey, institutionType = self.get_accountIdKey()
        url = BASE + Portfolio.format(accountIdKey=accountIdKey)
        resp = self._request(url=url, header_auth=True)
        if resp.status_code == 204:
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
        elif resp.status_code == 200:
            content = resp.json()
            if "Position" in content["PortfolioResponse"]["AccountPortfolio"]:
                position_data = content["PortfolioResponse"]["AccountPortfolio"][0]["Position"]
                for data in position_data:
                    data["account"] = str(self)
                    data["code"] = data["symbolDescription"]
                    data["qty"] = data["quantity"]
                    data["can_sell_qty"] = np.NaN
                    data["nominal_price"] = data["marketValue"]
                    data["cost_price"] = data["pricePaid"]
                    data["position_side"] = data["positionType"]
                    data["today_pl_val"] = data["daysGain"]
                    data["pl_val"] = data["totalGain"]
                    data["today_buy_qty"] = np.NaN
                    data["today_sell_qty"] = np.NaN
                    data["today_total_qty"] = data["todayQuantity"]
                    pos_df = data[
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
            return True
        elif resp.status_code != 200:
            raise Exception("Error Get Etrade Account Positions")

    def parse_order_info(self, order_info_dict):
        """
            Provide place orders
        """
        accountIdKey, institutionType = self.get_accountIdKey()
        consumerKey = self.consumer_key
        code = order_info_dict["symbol"].split(".")[1]
        trd_side = order_info_dict["side"]
        qty = int(order_info_dict["quantity"])
        market_session = order_info_dict["market_session"]

        if order_info_dict["price type"] == "Limit":
            order_type = "LIMIT"
            price = order_info_dict["price"]
            stop_price = None
        elif order_info_dict["price type"] == "Market":
            order_type = "MARKET"
            price = None
            stop_price = None
        elif order_info_dict["price type"] == "Stop Limit":
            order_type = "STOP_LIMIT"
            price = order_info_dict["price"]
            stop_price = order_info_dict["stop price"]
        elif order_info_dict["price type"] == "Stop":
            order_type = "STOP"
            price = None
            stop_price = order_info_dict["stop price"]

        if order_info_dict["time in force"] == "DAY":
            order_term = "GOOD_FOR_DAY"
        elif order_info_dict["time in force"] == "GTC":
            order_term = "GOOD_UNTIL_CANCEL"
        elif order_info_dict["time in force"] == "GTD":
            order_term = "GOOD_TILL_DATE"
        elif order_info_dict["time in force"] == "IOC":
            order_term = "IMMEDIATE_OR_CANCEL"
        elif order_info_dict["time in force"] == "FOK":
            order_term = "FILL_OR_KILL"

        preview_order = {
                        "price_type": order_type,
                        "order_term": order_term,
                        "symbol": code,
                        "order_action": trd_side,
                        "limit_price": price,
                        "stop_Price": stop_price,
                        "quantity": qty,
                        "marketSession": market_session,
                        "client_order_id": random.randint(1000000000, 9999999999)}

        preview_load = """<PreviewOrderRequest>
                               <orderType>EQ</orderType>
                               <clientOrderId>{0}</clientOrderId>
                               <Order>
                                   <allOrNone>false</allOrNone>
                                   <priceType>{1}</priceType>
                                   <orderTerm>{2}</orderTerm>
                                   <marketSession>{3}</marketSession>
                                   <stopPrice>{4}</stopPrice>
                                   <limitPrice>{5}</limitPrice>
                                   <Instrument>
                                       <Product>
                                           <securityType>EQ</securityType>
                                           <symbol>{6}</symbol>
                                       </Product>
                                       <orderAction>{7}</orderAction>
                                       <quantityType>QUANTITY</quantityType>
                                       <quantity>{8}</quantity>
                                   </Instrument>
                               </Order>
                         </PreviewOrderRequest>"""
        last_preview_load = preview_load.format(preview_order["client_order_id"], preview_order["price_type"],
                                                preview_order["order_term"], preview_order["marketSession"],
                                                preview_order["stop_Price"], preview_order["limit_price"],
                                                preview_order["symbol"], preview_order["order_action"],
                                                preview_order["quantity"])
        headers = {"Content-Type": "application/xml", "consumerKey": consumerKey}
        url = BASE + PreviewOrder.format(accountIdKey=accountIdKey)
        response = self._request(method="POST", url=url, header_auth=True, headers=headers, data=last_preview_load)
        data = response.json()
        PreviewId = data["PreviewOrderResponse"]["PreviewIds"][0]["previewId"]
        play_load = """<PlaceOrderRequest>
                           <orderType>EQ</orderType>
                           <clientOrderId>{0}</clientOrderId>
                           <PreviewIds>
                              <previewId>{1}</previewId>
                           </PreviewIds>
                           <Order>
                              <allOrNone>false</allOrNone>
                              <priceType>{2}</priceType>
                              <orderTerm>{3}</orderTerm>
                              <marketSession>{4}</marketSession>
                              <stopPrice>{5}</stopPrice>
                              <limitPrice>{6}</limitPrice>
                              <Instrument>
                                 <Product>
                                    <securityType>EQ</securityType>
                                    <symbol>{7}</symbol>
                                 </Product>
                                 <orderAction>{8}</orderAction>
                                 <quantityType>QUANTITY</quantityType>
                                 <quantity>{9}</quantity>
                              </Instrument>
                           </Order>
                       </PlaceOrderRequest>"""
        last_play_load = play_load.format(preview_order["client_order_id"], PreviewId,
                                          preview_order["price_type"], preview_order["order_term"],
                                          preview_order["marketSession"], preview_order["stop_Price"],
                                          preview_order["limit_price"], preview_order["symbol"],
                                          preview_order["order_action"], preview_order["quantity"])
        return last_play_load

    def place_order(self, order_info_dict):
        accountIdKey, institutionType = self.get_accountIdKey()
        consumerKey = self.consumer_key
        url = BASE + PlaceOrder.format(accountIdKey=accountIdKey)
        payload = self.parse_order_info(order_info_dict)
        headers = {"Content-Type": "application/xml", "consumerKey": consumerKey}
        resp = self._request(
            method="POST",
            url=url,
            header_auth=True,
            headers=headers,
            data=payload,
        )
        if resp.status_code == 200:
            return "OK"
        else:
            return "Error", str(resp.status_code) + str(resp.text)

    def get_today_deals(self, fromDate=None, toDate=None, params=None):
        accountIdKey, institutionType = self.get_accountIdKey()
        consumerKey = self.consumer_key
        url = BASE + Check_order.format(accountIdKey=accountIdKey)
        headers = {"consumerkey": consumerKey}
        resp = self._request(url, header_auth=True, headers=headers)
        if resp.status_code == 200:
            record = resp.json()
            if record:
                for information in record["OrdersResponse"]["Order"]:
                    information["code"] = information["OrderDetail"][0]["Instrument"][0]["Product"]["symbol"]
                    information["trd_side"] = information["OrderDetail"][0]["Instrument"][0]["orderAction"]
                    information["price"] = information["OrderDetail"][0]["orderValue"]
                    information["qty"] = int(information["OrderDetail"][0]["Instrument"][0]["filledQuantity"])
                    information["create_time"] = information["OrderDetail"][0]["placedTime"]
                    time_array = datetime.fromtimestamp(information["create_time"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                    information["create_time"] = time_array
                    information["status"] = information["OrderDetail"][0]["status"]
                    information["order_id"] = information["orderId"]
                record_pd = pd.json_normalize(information)
                return record_pd[
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

    def get_history_deals(self, dfrom, dto):
        return self.get_today_deals(fromDate=dfrom, toDate=dto)

    def get_active_orders(self):
        params_open = {"status": "OPEN"}
        return self.get_today_deals(params=params_open)

    def get_history_orders(self, dfrom, dto):
        params_executed = {"status": "EXECUTED"}
        return self.get_today_deals(fromDate=dfrom, toDate=dto, params=params_executed)

    def modify_order(self, modified_order_dict):
        client_order_id = random.randint(1000000000, 9999999999)
        order_id = modified_order_dict["order id"]
        code = modified_order_dict["code"]
        order_type = modified_order_dict["order type"]
        qty = modified_order_dict["qty"]
        price = modified_order_dict["price"]
        trd_side = modified_order_dict["side"]
        stop_price = modified_order_dict["aux price"]
        if modified_order_dict["order type"] == "LIMIT":
            order_type = "LIMIT"
            stop_price = None
        elif modified_order_dict["order type"] == "STOP":
            order_type = "STOP"
        elif modified_order_dict["order type"] == "STOP_LIMIT":
            order_type = "STOP_LIMIT"
        time_in_force = modified_order_dict["time in force"]
        market_session = modified_order_dict["market session"]
        change_preview_order = {"price_type": order_type,
                                "order_term": time_in_force,
                                "marketSession": market_session,
                                "symbol": code,
                                "order_action": trd_side,
                                "stopPrice": stop_price,
                                "limit_price": price,
                                "quantity": qty,
                                "client_order_id": client_order_id}
        change_preview_payload = """<PreviewOrderRequest>
                                       <orderType>EQ</orderType>
                                       <clientOrderId>{0}</clientOrderId>
                                       <Order>
                                           <allOrNone>false</allOrNone>
                                           <priceType>{1}</priceType>
                                           <orderTerm>{2}</orderTerm>
                                           <marketSession>{3}</marketSession>
                                           <stopPrice>{4}</stopPrice>
                                           <limitPrice>{5}</limitPrice>
                                           <Instrument>
                                               <Product>
                                                   <securityType>EQ</securityType>
                                                   <symbol>{6}</symbol>
                                               </Product>
                                               <orderAction>{7}</orderAction>
                                               <quantityType>QUANTITY</quantityType>
                                               <quantity>{8}</quantity>
                                           </Instrument>
                                       </Order>
                                   </PreviewOrderRequest>"""

        change_preview = change_preview_payload.format(change_preview_order["client_order_id"], change_preview_order["order_type"],
                                                       change_preview_order["time_in_force"], change_preview_order["marketSession"],
                                                       change_preview_order["stopPrice"], change_preview_order["limit_price"],
                                                       change_preview_order["symbol"], change_preview_order["order_action"],
                                                       change_preview_order["quantity"])
        accountIdKey, institutionType = self.get_accountIdKey()
        consumerKey = self.consumer_key
        url = BASE + Change_PreviewOrder.format(accountIdKey=accountIdKey, orderId=order_id)
        headers = {"Content-Type": "application/xml", "consumerKey": consumerKey}
        change_preview_response = self._request(method="PUT", url=url, header_auth=True, headers=headers, data=change_preview)
        xml = change_preview_response.text
        new_change = xmltodict.parse(xml)
        PreviewId = list(new_change["PreviewOrderResponse"]["PreviewIds"].values())[0]

        change_place_payload = """<PlaceOrderRequest>
                                   <orderType>EQ</orderType>
                                   <clientOrderId>{0}</clientOrderId>
                                   <PreviewIds>
                                      <previewId>{1}</previewId>
                                   </PreviewIds>
                                   <Order>
                                      <allOrNone>false</allOrNone>
                                      <priceType>{2}</priceType>
                                      <orderTerm>{3}</orderTerm>
                                      <marketSession>{4}</marketSession>
                                      <stopPrice>{5}</stopPrice>
                                      <limitPrice>{6}</limitPrice>
                                      <Instrument>
                                         <Product>
                                            <securityType>EQ</securityType>
                                            <symbol>{7}</symbol>
                                         </Product>
                                         <orderAction>{8}</orderAction>
                                         <quantityType>QUANTITY</quantityType>
                                         <quantity>{9}</quantity>
                                      </Instrument>
                                   </Order>
                                </PlaceOrderRequest>"""
        change_place = change_place_payload.format(change_preview_order["client_order_id"], PreviewId,
                                                   change_preview_order["order_type"], change_preview_order["time_in_force"],
                                                   change_preview_order["marketSession"], change_preview_order["stopPrice"],
                                                   change_preview_order["limit_price"], change_preview_order["symbol"],
                                                   change_preview_order["order_action"], change_preview_order["quantity"])
        place_url = BASE + Change_PlaceOrder.format(accountIdKey=accountIdKey, orderId=order_id)
        resp = self._request(method="PUT", url=place_url, header_auth=True, headers=headers, data=change_place)
        if resp.status_code == 200:
            return "已修改"

        else:
            raise Exception(str(resp.status_code))

    def cancel_order(self, order_id):
        accountIdKey, institutionType = self.get_accountIdKey()
        consumerKey = self.consumer_key
        payload = """<CancelOrderRequest>
                        <orderId>{0}</orderId>
                     </CancelOrderRequest>
                  """
        payload = payload.format(order_id)
        url = BASE + Cancel_order.format(accountIdKey=accountIdKey)
        headers = {"Content-Type": "application/xml", "consumerKey": consumerKey}
        resp = self._request(method="PUT", url=url, header_auth=True, headers=headers, data=payload)
        if resp.status_code == 200:
            return "已撤单"

        else:
            raise Exception(str(resp.status_code))

