from account.IB.ib_acc import *
import numpy as np
import requests
from datetime import date

ib_acc = IBAcc(
    username="ibapi586", password="WCH7KMxti$!ZZne", account_number="U9911586"
)


def test_ccp_session():
    url = (
        BASE
        + "ccp/auth/init"
        # + "compete=true&locale=en_US&mac=98-43-FA-55-4A-98&machineID=C7374624-64E7-468C-B0EF-3D590B9B301E&username=-"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "compete": True,
        "locale": "en_US",
        "mac": "98-43-FA-55-4A-98",
        "machineID": "C7374624-64E7-468C-B0EF-3D590B9B301E",
        "username": "-",
    }
    ib_acc.session._reconnect()
    resp = requests.request(
        method="POST", url=url, headers=headers, data=payload, verify=False
    )

    if resp.status_code == 200:
        return resp.text
    else:
        return resp.status_code


def get_acc_asset():
    url = BASE + SUMMARY.format(accountID=ib_acc.account_number)
    resp = ib_acc._request(method="GET", url=url)
    if resp.status_code == 200:
        data = resp.json()
        return round(data["availablefunds"]["amount"], 3)


def test_get_pos():

    pageID = 0
    while True:
        # pos_df = pd.DataFrame()
        url = BASE + POSITIONS.format(accountID=ib_acc.account_number, pageID=pageID)
        logging.info(url)
        resp = ib_acc._request(method="GET", url=url)
        if resp.status_code == 200:
            data = resp.json()
            logging.info(data)
            if len(data) == 0:
                break
            else:
                df = pd.DataFrame(data)
                logging.info(df)
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
                df.insert(0, column="account", value=str(ib_acc))
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
                ib_acc.position = pd.concat([ib_acc.position, pos_df]).reset_index(
                    drop=True
                )
                logging.info(ib_acc.position)
                pageID = pageID + 1
        else:
            raise Exception(str(resp.status_code) + str(resp.text))
    logging.info(ib_acc.position)
    return True


def get_active_orders():
    url = BASE + ORDERS
    resp = ib_acc._request(method="GET", url=url)
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
                "create_time",
                "aux_price",
                "order_id",
            ]
        ].sort_values(by="create_time", ascending=False)


def get_trades():
    url = BASE + TRADES
    resp = ib_acc._request(method="GET", url=url)
    data = resp.json()
    df = pd.DataFrame(data)
    df = df[["symbol", "side", "price", "size", "trade_time_r", "order_ref"]]
    df["code"] = df["symbol"]
    df["trd_side"] = df["side"]
    df["qty"] = df["size"]
    df["create_time"] = df["trade_time_r"].apply(
        lambda x: datetime.fromtimestamp(int(x) / 1000)
    )

    df["status"] = pd.NA
    df["order_id"] = df["order_ref"]
    df["date"] = df["create_time"].apply(lambda x: x.date())
    today = date.today()
    df = df.loc[df["date"] == today]
    return df


def cancel_order(order_id=151798204):

    url = BASE + CANCEL_ORDER.format(accountID=ib_acc.account_number, orderID=order_id)
    resp = ib_acc._request(method="DELETE", url=url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return resp.status_code


if __name__ == "__main__":
    ib_acc.session._reconnect()
    # logging.info(cancel_order())
