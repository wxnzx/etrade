import sys
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QTableView,
    QAbstractItemView,
    QPushButton,
    QTabBar,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5 import QtGui
import pandas as pd
import os
import json
from datetime import datetime, timedelta
from UI.UI_order_details import Ui_Form
from UI.data_model import pandasModel, OrderModel
from UI.window_lang import ODT, CMT
from subwindow.modify_order_window import ModifyOrderWindow
from utils.worker.order_thread import (
    OrderThread,
    Sync2DBThread,
    CancelOrderThread,
    ModifyOrderThread,
)
import logging

logging.basicConfig(level=logging.INFO)


class OrderDetails(QWidget, Ui_Form):

    broker_account_list = []
    LANGUAGE = "CN"
    aurora_account = None
    db_list = []
    signal_window_failed = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Your code will go here

        self.setupUi(self)
        self.add_tab()
        self.resize(1200, 400)
        self.move(10, 410)

        # 载入模板
        self.load_layout()
        self.initialize()

        self.all_acc_orders = dict()
        self.all_acc_deals = dict()
        self.clicked_row = None
        self.clicked_model = None
        self.thread = {}
        self.populate_account_list()
        self.sync_to_db()
        # self.get_acc_orders()
        self.listWidget_acc.itemDoubleClicked.connect(self.refresh_account_view)
        self.tab.currentChanged.connect(self.tab_changed)
        self.tab.setCurrentIndex(0)
        self.tab_changed()
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        try:
            self.tableView.doubleClicked.disconnect()
        except TypeError:
            pass
        self.tableView.doubleClicked.connect(self.on_order_clicked)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.resizeColumnsToContents()
        self.dateEdit_from.dateChanged.connect(self.on_dateEdit_changed)
        self.dateEdit_to.dateChanged.connect(self.on_dateEdit_changed)
        self.show()

    def add_tab(self):
        self.tab = QTabBar(self)
        self.tab.addTab(ODT.tab_OA[self.LANGUAGE])
        self.tab.addTab(ODT.tab_OT[self.LANGUAGE])
        self.tab.addTab(ODT.tab_OH[self.LANGUAGE])
        self.tab.addTab(ODT.tab_DT[self.LANGUAGE])
        self.tab.addTab(ODT.tab_DH[self.LANGUAGE])
        self.tab.setShape(QTabBar.TriangularNorth)
        self.horizontalLayout_tab = QHBoxLayout()
        self.horizontalLayout_tab.addWidget(self.tab)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_tab.addItem(spacerItem)
        self.verticalLayout_2.insertLayout(0, self.horizontalLayout_tab)

    def initialize(self):
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
        self.Qyesterday = QDate(year, month, day)
        self.dateEdit_from.setDate(self.Qyesterday)
        self.dateEdit_to.setDate(self.Qyesterday)
        self.setWindowTitle(f"{ODT.window_title[self.LANGUAGE]}")
        self.listWidget_acc.addItem(f"{ODT.account_list_widget[self.LANGUAGE]}")
        self.label_CM.setText(f"{ODT.CM[self.LANGUAGE]}")

    def sync_to_db(self):
        self.thread[3] = Sync2DBThread(
            aurora_account=self.aurora_account,
            broker_list=self.broker_account_list,
            db_list=self.db_list,
        )
        self.thread[3].failed.connect(self.on_sync_failed)
        self.thread[3].start()

    def on_sync_failed(self):
        QMessageBox.critical(self, "数据库同步错误", "请关闭软件")
        self.thread[3].stop()
        self.signal_window_failed.emit()

    def on_order_clicked(self, clickedIndex):
        self.clicked_row = clickedIndex.row()
        self.clicked_model = clickedIndex.model()
        selected_account = self.order_df.iloc[self.clicked_row, 0]
        for broker_obj in self.broker_account_list:
            if str(broker_obj) == selected_account:
                self.selected_broker_obj = broker_obj
        order_id = self.order_df.iloc[self.clicked_row, -1]
        code = self.order_df.iloc[self.clicked_row, 1]
        order_type = self.order_df.iloc[self.clicked_row, 3]
        trd_side = self.order_df.iloc[self.clicked_row, 2]
        qty = self.order_df.iloc[self.clicked_row, 5]
        price = self.order_df.iloc[self.clicked_row, 4]
        aux_price = self.order_df.iloc[self.clicked_row, -2]
        time_in_force = self.order_df.iloc[self.clicked_row, -5]
        market_session = self.order_df.iloc[self.clicked_row, -4]

        CM_box = QMessageBox()
        CM_box.setWindowTitle(CMT.window_title[self.LANGUAGE])
        CM_box.setText(CMT.text[self.LANGUAGE])
        CM_box.addButton(
            QPushButton(CMT.button_cancel[self.LANGUAGE]), QMessageBox.YesRole
        )
        CM_box.addButton(
            QPushButton(CMT.button_modify[self.LANGUAGE]), QMessageBox.NoRole
        )
        CM_box.addButton(
            QPushButton(CMT.button_discard[self.LANGUAGE]), QMessageBox.RejectRole
        )
        ret = CM_box.exec_()
        logging.info(ret)
        if ret == 0:
            ret_cancel = QMessageBox.critical(
                self,
                CMT.confirm[self.LANGUAGE][0],
                CMT.confirm[self.LANGUAGE][1],
                QMessageBox.Yes | QMessageBox.No,
            )
            if ret_cancel == QMessageBox.Yes:
                logging.info("Cancel Order")
                logging.info(order_id)
                self.cancel_order(order_id)
            else:
                return
        if ret == 1:
            logging.info("Modify Order")
            logging.info(order_id)

            self.modify_window = ModifyOrderWindow(
                order_id,
                code,
                order_type,
                trd_side,
                qty,
                price,
                aux_price,
                time_in_force,
                market_session,
                str(self.selected_broker_obj),
            )
            self.modify_window.pushButton_modify.clicked.connect(self.modify_confirmed)
            self.modify_window.pushButton_cancel.clicked.connect(self.modify_canceled)
            self.modify_window.show()

        if ret == 2:
            return

    def modify_confirmed(self):
        self.modify_window.close()

        modified_order_dict = dict()
        modified_order_dict["qty"] = self.modify_window.spinBox_qty.value()
        modified_order_dict["order id"] = self.modify_window.lineEdit_orderID.text()
        modified_order_dict["price"] = self.modify_window.doubleSpinBox_price.value()
        modified_order_dict[
            "aux price"
        ] = self.modify_window.doubleSpinBox_sprice.value()

        # TD 修改订单，需要更多参数
        modified_order_dict["code"] = self.modify_window.lineEdit_sym.text()
        modified_order_dict["side"] = self.modify_window.lineEdit_side.text()
        modified_order_dict["order type"] = self.modify_window.lineEdit_orderType.text()
        modified_order_dict["time in force"] = self.modify_window.lineEdit_tif.text()
        modified_order_dict[
            "market session"
        ] = self.modify_window.lineEdit_session.text()
        self.modify_order(modified_order_dict)

    def modify_canceled(self):
        self.modify_window.close()

    def populate_account_list(self):
        if len(self.broker_account_list) > 0:
            for broker_obj in self.broker_account_list:
                # self.listWidget_acc.addItem(f"{broker_obj.broker}-{broker_obj.username}")
                self.listWidget_acc.addItem(str(broker_obj))

    def tab_changed(self):
        if self.tab.currentIndex() == 0:
            logging.info("0")
            self.groupBox_fitler.setVisible(False)
            self.label_CM.setVisible(True)
            self.get_acc_OA()
            try:
                self.tableView.doubleClicked.disconnect()
            except TypeError:
                pass
            self.tableView.doubleClicked.connect(self.on_order_clicked)
        elif self.tab.currentIndex() == 1:
            logging.info("1")
            self.groupBox_fitler.setVisible(False)
            self.label_CM.setVisible(True)
            self.get_acc_OT()
            try:
                self.tableView.doubleClicked.disconnect()
            except TypeError:
                pass
            self.tableView.doubleClicked.connect(self.on_order_clicked)

        elif self.tab.currentIndex() == 2:
            logging.info("2")
            self.groupBox_fitler.setVisible(True)
            self.label_CM.setVisible(True)
            self.get_acc_OH()
            try:
                self.tableView.doubleClicked.disconnect()
            except TypeError:
                pass
            self.tableView.doubleClicked.connect(self.on_order_clicked)
        elif self.tab.currentIndex() == 3:
            logging.info("3")
            self.groupBox_fitler.setVisible(False)
            self.label_CM.setVisible(False)
            self.get_acc_DT()
            try:
                self.tableView.doubleClicked.disconnect()
            except TypeError:
                pass
        elif self.tab.currentIndex() == 4:
            logging.info("4")
            self.groupBox_fitler.setVisible(True)
            self.label_CM.setVisible(False)
            self.get_acc_DH()
            try:
                self.tableView.doubleClicked.disconnect()
            except TypeError:
                pass

    def on_dateEdit_changed(self):
        if self.dateEdit_from.date() > self.dateEdit_to.date():
            self.dateEdit_from.setDate(self.Qyesterday)
            self.dateEdit_to.setDate(self.Qyesterday)
            QMessageBox.warning(self, "日期错误", "起始日期应小于截止日期")
        else:
            if self.tab.currentIndex() == 2:
                self.get_acc_OH()
            elif self.tab.currentIndex() == 4:
                self.get_acc_DH()

    def get_acc_OT(self):
        try:
            self.thread[0].stop()
        except KeyError:
            pass
        self.thread[0] = OrderThread(
            aurora_account=self.aurora_account,
            broker_list=self.broker_account_list,
            order=True,
            today=True,
        )
        self.thread[0].start()
        self.thread[0].signal_acc_orders.connect(self.on_acc_orders_changed)
        self.thread[0].failed.connect(self.on_acc_orders_failed)

    def get_acc_OA(self):
        try:
            self.thread[0].stop()
        except KeyError:
            pass
        self.thread[0] = OrderThread(
            broker_list=self.broker_account_list, order=True, today=None
        )
        self.thread[0].start()
        self.thread[0].signal_acc_orders.connect(self.on_acc_orders_changed)
        self.thread[0].failed.connect(self.on_acc_orders_failed)

    def get_acc_OH(self):
        try:
            self.thread[0].stop()
        except KeyError:
            pass
        self.thread[0] = OrderThread(
            broker_list=self.broker_account_list,
            order=True,
            today=False,
            date=[
                self.dateEdit_from.date().toPyDate().strftime("%Y-%m-%d"),
                self.dateEdit_to.date().toPyDate().strftime("%Y-%m-%d"),
            ],
        )
        self.thread[0].start()
        self.thread[0].signal_acc_orders.connect(self.on_acc_orders_changed)
        self.thread[0].failed.connect(self.on_acc_orders_failed)

    def get_acc_DT(self):

        try:
            self.thread[0].stop()
        except KeyError:
            pass
        self.thread[0] = OrderThread(
            broker_list=self.broker_account_list, order=False, today=True
        )
        self.thread[0].start()
        self.thread[0].signal_acc_orders.connect(self.on_acc_orders_changed)
        self.thread[0].failed.connect(self.on_acc_orders_failed)

    def get_acc_DH(self):
        try:
            self.thread[0].stop()
        except KeyError:
            pass
        self.thread[0] = OrderThread(
            broker_list=self.broker_account_list,
            order=False,
            today=False,
            date=[
                self.dateEdit_from.date().toPyDate().strftime("%Y-%m-%d"),
                self.dateEdit_to.date().toPyDate().strftime("%Y-%m-%d"),
            ],
        )
        self.thread[0].start()
        self.thread[0].signal_acc_orders.connect(self.on_acc_orders_changed)
        self.thread[0].failed.connect(self.on_acc_orders_failed)

    def on_acc_orders_changed(self, acc_orders_dict):
        if (
            self.tab.currentIndex() == 0
            or self.tab.currentIndex() == 1
            or self.tab.currentIndex() == 2
        ):
            if acc_orders_dict["index"] not in self.all_acc_orders.keys():
                self.all_acc_orders[acc_orders_dict["index"]] = acc_orders_dict[
                    "orders"
                ]
            else:
                temp_dict = {}
                for key, value in self.all_acc_orders.items():
                    if acc_orders_dict["index"] == key:
                        temp_dict[key] = acc_orders_dict["orders"]
                    else:
                        temp_dict[key] = value
                self.all_acc_orders = temp_dict
        else:
            if acc_orders_dict["index"] not in self.all_acc_deals.keys():
                self.all_acc_deals[acc_orders_dict["index"]] = acc_orders_dict["orders"]
            else:
                temp_dict = {}
                for key, value in self.all_acc_deals.items():
                    if acc_orders_dict["index"] == key:
                        temp_dict[key] = acc_orders_dict["orders"]
                    else:
                        temp_dict[key] = value
                self.all_acc_deals = temp_dict
        self.refresh_account_view()

    def on_acc_orders_failed(self):
        self.thread[0].stop()
        self.signal_window_failed.emit()

    def refresh_account_view(self):
        selected_account = self.listWidget_acc.currentItem().text()
        if (
            self.tab.currentIndex() == 0
            or self.tab.currentIndex() == 1
            or self.tab.currentIndex() == 2
        ):
            temp_order_df = pd.DataFrame(columns=ODT.order_columns[self.LANGUAGE])
            all_acc = self.all_acc_orders
        else:
            temp_order_df = pd.DataFrame(columns=ODT.deal_columns[self.LANGUAGE])
            all_acc = self.all_acc_deals
        new_cols = {
            x: y
            for x, y in zip(
                all_acc[list(all_acc)[0]].columns,
                temp_order_df.columns,
            )
        }
        if selected_account == "All Accounts" or selected_account == "所有账户":
            for key, value in all_acc.items():
                temp_order_df = pd.concat(
                    [temp_order_df, value.rename(columns=new_cols)]
                )

            # jimmy 风控要求所有券商的按订单时间排序，而不是按券商排序
            temp_order_df.reset_index(drop=True, inplace=True)
            temp_order_df.sort_values(
                by=list(temp_order_df)[-3], ascending=False, inplace=True
            )
        else:
            for key, value in all_acc.items():
                if selected_account == key:
                    temp_order_df = value.rename(columns=new_cols)
        self.order_df = temp_order_df
        if self.tab.currentIndex() in [0, 1]:
            self.tableView.setModel(OrderModel(temp_order_df))
            self.tableView.resizeColumnsToContents()
        else:
            self.tableView.setModel(pandasModel(temp_order_df))
            self.tableView.resizeColumnsToContents()

    def cancel_order(self, order_id):
        self.thread[1] = CancelOrderThread(
            broker_obj=self.selected_broker_obj, order_id=order_id
        )
        self.thread[1].start()
        self.thread[1].failed.connect(self.cancel_order_failed)
        self.thread[1].finished.connect(self.cancel_order_successful)

    def cancel_order_failed(self, msg):
        self.thread[1].stop()
        QMessageBox.critical(self, "取消订单失败", msg)

    def cancel_order_successful(self):
        self.thread[1].stop()
        QMessageBox.information(self, "成功", "订单已成功取消")

    def modify_order(self, modified_order_dict):
        self.thread[2] = ModifyOrderThread(
            broker_obj=self.selected_broker_obj, modified_order=modified_order_dict
        )
        self.thread[2].start()
        self.thread[2].failed.connect(self.modify_failed)
        self.thread[2].finished.connect(self.modify_finished)

    def modify_failed(self, msg):
        self.thread[2].stop()
        QMessageBox.critical(self, "修改订单失败", msg)

    def modify_finished(self):
        self.thread[2].stop()
        QMessageBox.information(self, "成功", "订单已成功修改")

    def load_layout(self):
        file_path = r"temp/layout.json"
        if os.path.exists(file_path) == False:
            pass
        else:
            with open(file_path, "r") as layoutF:
                layout_obj = json.load(layoutF)
            if "order_detail_window" in layout_obj:
                self.move(
                    layout_obj["order_detail_window"]["x"],
                    layout_obj["order_detail_window"]["y"],
                )
                self.resize(
                    layout_obj["order_detail_window"]["w"],
                    layout_obj["order_detail_window"]["h"],
                )

    def closeEvent(self, event):
        try:
            self.thread[0].stop()
        except KeyError:
            pass
        try:
            self.thread[1].stop()
        except KeyError:
            pass
        try:
            self.thread[2].stop()
        except KeyError:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OrderDetails()
    sys.exit(app.exec_())
