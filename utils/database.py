import os
import pymysql
import time
import pandas as pd
from sqlalchemy import create_engine


class AuroraDB(object):
    def __init__(self, db_list):
        dbhost = db_list[0]
        dbuser = db_list[1]
        dbpass = db_list[2]
        # Set database credentials.
        creds = {
            "usr": dbuser,
            "pwd": dbpass,
            "hst": dbhost,
            "prt": 3306,
            "dbn": "client_data",
        }
        # MySQL conection string.
        connstr = "mysql+pymysql://{usr}:{pwd}@{hst}:{prt}/{dbn}"
        # Create sqlalchemy engine for MySQL connection.
        self.engine = create_engine(connstr.format(**creds))
        self.db = pymysql.connect(
            host=dbhost, user=dbuser, password=dbpass, database="client_data"
        )

    def insert_cash(self,cash):
        cash.to_sql(
            name="assets", con=self.engine, index=False, if_exists="append"
        )

    def insert_position(self, position):
        position.to_sql(
            name="positions", con=self.engine, index=False, if_exists="append"
        )

    def insert_order(self, order):
        order.to_sql(name="orders", con=self.engine, index=False, if_exists="append")

    def insert_deal(self, deal):
        deal.to_sql(name="deals", con=self.engine, index=False, if_exists="append")

    def insert_account(self, aurora_account):
        aurora_account.to_sql(
            name="account", con=self.engine, index=False, if_exists="append"
        )


if __name__ == "__main__":
    d = {
        "username": ["lzl", "lzl"],
        "account": ["futu1", "futu2"],
        "code": ["US.JD", "US.JD"],
        "cost": [123, 111],
        "qty": [100, 100],
        "current_price": [120, 90],
    }
    pos = pd.DataFrame(data=d)
    db_obj = AuroraDB()
    db_obj.insert_position(pos)
