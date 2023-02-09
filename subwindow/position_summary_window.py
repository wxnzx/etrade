import sys
import os
import json
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtCore import pyqtSignal
import pandas as pd
from UI.UI_position_summary import Ui_Form
from UI.data_model import pandasModel
from utils.worker.position_thread import PositionThread, Sync2DBThread
from UI.window_lang import PST
import logging

logging.basicConfig(level=logging.INFO)


class PositionSummary(QWidget, Ui_Form):
    aurora_account = None
    broker_account_list = []
    LANGUAGE = "CN"
    db_list = []
    signal_window_failed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Your code will go here

        self.setupUi(self)
        self.resize(1200, 400)
        self.move(10, 850)
        self.load_layout()
        self.initialize()

        self.all_acc_pos = dict()
        self.thread = {}
        self.sync_to_db()
        self.populate_account_list()
        self.get_acc_pos()
        self.account_list_widget.itemDoubleClicked.connect(self.refresh_account_view)
        self.show()

    def initialize(self):
        self.setWindowTitle(f"{PST.window_title[self.LANGUAGE]}")
        self.setStyleSheet("QLineEdit:read-only{background: palette(window);}")
        self.label_chooseAccount.setText(
            f'<html><head/><body><p><span style=" font-weight:600;">{PST.label_chooseAccount[self.LANGUAGE]}</span></p></body></html>'
        )
        self.account_list_widget.addItem(f"{PST.account_list_widget[self.LANGUAGE]}")
        self.label_totalAsset.setText(f"{PST.total_asset[self.LANGUAGE]}")
        self.label_cash.setText(f"{PST.cash[self.LANGUAGE]}")
        self.label_marketVal.setText(f"{PST.market_val[self.LANGUAGE]}")
        self.table_columns = PST.table_columns[self.LANGUAGE]

    def sync_to_db(self):
        self.thread[0] = Sync2DBThread(
            broker_list=self.broker_account_list,
            aurora_account=self.aurora_account,
            db_list=self.db_list,
        )
        self.thread[0].start()
        self.thread[0].failed.connect(self.on_sync_failed)

    def on_sync_failed(self):
        self.signal_window_failed.emit()
        self.thread[0].stop()

    def populate_account_list(self):
        if len(self.broker_account_list) > 0:
            for broker_obj in self.broker_account_list:
                self.account_list_widget.addItem(str(broker_obj))
        self.account_list_widget.setCurrentRow(0)

    def get_acc_pos(self):
        self.thread[1] = PositionThread(
            broker_list=self.broker_account_list, aurora_account=self.aurora_account
        )
        self.thread[1].start()
        self.thread[1].signal_acc_pos.connect(self.on_acc_pos_emitted)
        self.thread[1].signal_acc_asset.connect(self.on_acc_asset_emitted)
        self.thread[1].failed.connect(self.on_acc_pos_failed)
        # self.thread.failed.connect(lambda: self.thread.stop)

    def on_acc_pos_emitted(self):
        logging.info("refreshing pos")
        # self.sync_to_db()
        selected_account = self.account_list_widget.currentItem().text()
        if selected_account == "All Accounts" or selected_account == "所有账户":
            temp_pos_df = pd.DataFrame(columns=PST.table_columns[self.LANGUAGE])
            for broker_obj in self.broker_account_list:
                new_cols = {
                    x: y
                    for x, y in zip(broker_obj.position.columns, temp_pos_df.columns)
                }
                temp_pos_df = pd.concat(
                    [temp_pos_df, broker_obj.position.rename(columns=new_cols)]
                )
        else:
            for broker_obj in self.broker_account_list:
                if str(broker_obj) == selected_account:
                    new_cols = {
                        x: y
                        for x, y in zip(
                            broker_obj.position.columns,
                            PST.table_columns[self.LANGUAGE],
                        )
                    }
                    temp_pos_df = broker_obj.position.rename(columns=new_cols)
        # total_temp_df = pd.DataFrame()
        # total_temp_df[PST.table_columns_total[self.LANGUAGE][0]] = temp_pos_df.loc[
        #     :, temp_pos_df.columns.isin(["UNREALIZED PL", "未实现盈亏"])
        # ].sum()
        # total_temp_df[PST.table_columns_total[self.LANGUAGE][1]] = temp_pos_df.loc[
        #     :, temp_pos_df.columns.isin(["REALIZED PL", "已实现盈亏"])
        # ].sum()

        self.account_view.setModel(pandasModel(temp_pos_df))
        self.account_view.resizeColumnsToContents()
        # self.tableView_total.setModel(pandasModel(total_temp_df))
        # self.tableView_total.resizeColumnsToContents()

    def on_acc_asset_emitted(self):
        logging.info("refreshing asset")
        temp_total_assets = 0
        temp_cash = 0
        temp_market_val = 0
        selected_account = self.account_list_widget.currentItem().text()
        if selected_account == "All Accounts" or selected_account == "所有账户":
            for broker_obj in self.broker_account_list:
                temp_total_assets += broker_obj.total_assets
                temp_cash += broker_obj.cash
                temp_market_val += broker_obj.market_val

        else:
            for broker_obj in self.broker_account_list:
                if str(broker_obj) == selected_account:
                    temp_total_assets = broker_obj.total_assets
                    temp_cash = broker_obj.cash
                    temp_market_val = broker_obj.market_val

        self.lineEdit_totalAsset.setText(str(temp_total_assets))
        self.lineEdit_cash.setText(str(temp_cash))
        self.lineEdit_marketVal.setText(str(temp_market_val))

    def on_acc_pos_failed(self):
        self.thread[1].stop()
        self.signal_window_failed.emit()

    def refresh_account_view(self):
        self.on_acc_pos_emitted()
        self.on_acc_asset_emitted()

    def load_layout(self):
        file_path = r"temp/layout.json"
        if os.path.exists(file_path) == False:
            pass
        else:
            with open(file_path, "r") as layoutF:
                layout_obj = json.load(layoutF)
            if "position_summary_window" in layout_obj:
                self.move(
                    layout_obj["position_summary_window"]["x"],
                    layout_obj["position_summary_window"]["y"],
                )
                self.resize(
                    layout_obj["position_summary_window"]["w"],
                    layout_obj["position_summary_window"]["h"],
                )

    def closeEvent(self, event):
        try:
            self.thread[1].stop()
        except KeyError:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    PositionSummary.broker_account_list = []
    w = PositionSummary()
    sys.exit(app.exec_())
