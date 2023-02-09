import logging
import urllib3
import sys
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QMdiArea,
    QTextBrowser,
    QMessageBox,
    QApplication)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QEvent
from subwindow.level_one_window import LevelOne
from subwindow.login_window import LoginWindow
from subwindow.broker_window import BrokerWindow
from subwindow.position_summary_window import PositionSummary
from subwindow.order_detail_window import OrderDetails
from account import AuroraAccount, BrokerBase
from utils.worker.main_sync_thread import Sync2DBThread
from utils.worker.login_request_thread import LoginRqstThread
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv, set_key
formatter = "[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)"
# logging.basicConfig(
#     filename="log.txt",
#     filemode="a",
#     format=formatter,
#     datefmt="%H:%M:%S",
#     level=logging.ERROR,
# )
logging.basicConfig(level=logging.INFO, format=formatter)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ["NUMEXPR_MAX_THREADS"] = r"12"


class MainWindow(QMainWindow):
    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self._socket_ready = False
        self.thread = {}
        dotenv_path = join(dirname(os.path.realpath(sys.argv[0])), ".env")
        logging.info(dotenv_path)
        load_dotenv(dotenv_path)
        dbhost = os.environ.get("HOST_RDS")
        dbuser = os.environ.get("USERNAME_RDS")
        dbpass = os.environ.get("PASSWORD_RDS")
        self.db_list = [dbhost, dbuser, dbpass]
        self.LANGUAGE = os.environ.get("LANGUAGE")
        self.host_server = os.environ.get("HOST_SERVER")
        self.port_server = os.environ.get("PORT_SERVER")
        LoginWindow.LANGUAGE = self.LANGUAGE
        LoginWindow.host_server = self.host_server
        LoginWindow.port_server = int(self.port_server)
        BrokerWindow.LANGUAGE = self.LANGUAGE
        LevelOne.LANGUAGE = self.LANGUAGE
        PositionSummary.LANGUAGE = self.LANGUAGE
        PositionSummary.db_list = self.db_list
        OrderDetails.LANGUAGE = self.LANGUAGE
        OrderDetails.db_list = self.db_list
        self.initialize()
        self.login_window = LoginWindow()
        self.broker_window = BrokerWindow()

        # login_msgBox
        self.login_msgBox = QMessageBox()
        self.login_msgBox.move(
            self.login_window.geometry().x()
            + int(self.login_window.geometry().width() / 4),
            self.login_window.geometry().y()
            + int(self.login_window.geometry().height() / 4),
        )
        self.level_one_window_list = []
        self.broker_window.hide()
        self.login_window.show()
        self.connect_slots()
        logging.info(self.LANGUAGE)

    def initialize(self):
        self.setWindowTitle("AURORA POLARIS")
        # self.resize(350, 300)
        self.setFixedSize(450, 300)
        self.move(760, 70)
        # Main UI code goes here
        self.aurora_account_main = None
        self.broker_list_main = []
        # Menubar
        menubar = self.menuBar()  # QMenuBar
        # window_menu = menubar.addMenu("Windows")  # QMenu

        open_window_menu = menubar.addMenu("打开窗口")

        open_window_menu.addAction("添加券商账户", self.open_broker)
        open_window_menu.addAction("Level I", self.open_level_one)
        # open_window_menu.addAction("Level II", self.open_level_two)
        open_window_menu.addAction("持仓", self.open_position_summary)
        open_window_menu.addAction("订单详情", self.open_order_details)

        # minimize and normal sub
        open_window_menu.addSeparator()
        open_window_menu.addAction("最小化子窗口", self.minimize_sub_window)
        open_window_menu.addAction("还原子窗口", self.normal_sub_window)

        settings_menu = menubar.addMenu("设置")
        language_selection_menu = settings_menu.addMenu("语言选择")
        language_selection_menu.addAction("中文", self.language_CN)
        language_selection_menu.addAction("English", self.language_EN)
        language_selection_menu.setEnabled(False)

        # layout
        settings_menu.addAction("保存模板", self.save_layout)

        menubar.addAction("退出", self.close)

        # Adding widgets to main window

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setHtml(
            """
            <div style="font-family: Microsoft YaHei, Times New Roman"}>
            <h1><font size="5" color="#2B1C5C"><black>欢迎使用AURORA POLARIS!</black></font></h1>
            <ul>
                <li><font size="4">开启窗口请点击菜单栏&ldquo;打开窗口&rdquo;</font></li>
                <li><font size="4">LEVEL ONE窗口最多可开启8个</font></li>
                <li><font size="4" color="red">退出该程序前不要退出FutuOpenD！</font></li>
                <li><font size="4" color="red">关闭本窗口将退出该程序！</font></li>
            </ul>
            </div>
            """
        )
        self.textBrowser.setReadOnly(True)
        self.mdiArea.addSubWindow(self.textBrowser)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)

    def connect_slots(self):
        # self.login_window.connect_button.clicked.connect(self.start_main_connection_worker)
        self.login_window.submit_button.clicked.connect(self.on_login_submitted)
        self.login_window.authenticated.connect(self.aurora_login_success)
        self.broker_window.authenticated.connect(self.verified_broker_existed)
        self.broker_window.deleted.connect(self.delete_broker_account)
        self.broker_window.delete_local_button.clicked.connect(self.on_delete_local)

    def on_delete_local(self):
        self.close_all_windows()
        self.close()

    def language_CN(self):
        dotenv_path = ".env"
        if self.LANGUAGE == "CN":
            pass
        else:
            ret = QMessageBox.question(
                self, "重启", "请重新打开软件以使设置生效", QMessageBox.Yes | QMessageBox.No
            )
            if ret == QMessageBox.Yes:
                set_key(dotenv_path, "LANGUAGE", "CN")
                self.close()
            else:
                return

    def language_EN(self):
        dotenv_path = ".env"
        if self.LANGUAGE == "EN":
            pass
        else:
            ret = QMessageBox.question(
                self, "Restart", "Please restart", QMessageBox.Yes | QMessageBox.No
            )
            if ret == QMessageBox.Yes:
                set_key(dotenv_path, "LANGUAGE", "EN")
                self.close()
            else:
                return

    def on_login_submitted(self):
        # self.start_main_connection_worker()
        self.login_window.submit_button.setEnabled(False)
        self.login_window.textBrowser.clear()
        self.start_login_request_worker()

    def on_login_status_updated(self, msg):
        self.login_window.textBrowser.insertPlainText(msg)
        # 滚动条移动到结尾
        self.login_window.textBrowser.moveCursor(QTextCursor.End)

    # --------------start loggin request worker -------------------
    def start_login_request_worker(self):
        self.address = (
            str(self.login_window.server_ip),
            int(self.login_window.server_port),
        )
        username = str(self.login_window.username_edit.text())
        password = str(self.login_window.password_edit.text())
        self.aurora_account_main = AuroraAccount(username, password)
        login_info = {"username": username, "password": password}
        login_rqst_msg = json.dumps({"status": "login_request", "content": login_info})
        self.thread[2] = LoginRqstThread(
            parent=None, address=self.address, rqst_msg=login_rqst_msg
        )
        self.thread[2].start()
        self.thread[2].failed.connect(self.on_login_connection_failed)
        self.thread[2].signal_login_result.connect(self.on_login_result_emitted)
        self.thread[2].signal_login_status.connect(self.on_login_status_updated)

    def on_login_connection_failed(self, msg):
        logging.info("login connection failed")
        self.thread[2].stop()
        self.login_msgBox.setIcon(QMessageBox.Critical)
        self.login_msgBox.setWindowTitle("登录失败")
        self.login_msgBox.setText(f"{msg}")
        self.login_msgBox.exec_()
        self.login_window.submit_button.setEnabled(True)
        # self.close_all_windows()

    def on_login_result_emitted(self, msg_json):
        msg = json.loads(msg_json)
        self.thread[2].stop()
        if msg["status"] == "login_result":
            self.login_window.submit_button.setEnabled(True)
            if msg["content"]["login"] == "T":
                self.token = msg["content"]["token"]
                self.aurora_account_main.logged_in = True
                self.aurora_account_main.account_tier = msg["content"]["account_tier"]
                self.login_window.authenticated.emit()
            elif msg["content"]["login"] == "F":
                self.login_msgBox.setIcon(QMessageBox.Critical)
                self.login_msgBox.setWindowTitle("登录失败")
                self.login_msgBox.setText("请检查用户名和密码")
                self.login_msgBox.exec_()
                self.thread[2].signal_login_status.emit("登录失败\n")
            elif msg["content"]["login"] == "U":
                self.login_msgBox.setIcon(QMessageBox.Critical)
                self.login_msgBox.setWindowTitle("登录失败")
                self.login_msgBox.setText("服务器错误，请稍后再试")
                self.login_msgBox.exec_()
                self.thread[2].signal_login_status.emit("登录失败\n")
            else:
                self.login_msgBox.setIcon(QMessageBox.Critical)
                self.login_msgBox.setWindowTitle("错误")
                self.login_msgBox.setText("服务器返回未认证值")
                self.login_msgBox.exec_()
                self.thread[2].signal_login_status.emit("请联系Aurora Polaris\n")

    def aurora_login_success(self):
        self.thread[1] = Sync2DBThread(
            aurora_account=self.aurora_account_main.username, db_list=self.db_list
        )
        self.thread[1].start()
        self.thread[1].failed.connect(self.on_sync_login_failed)
        self.login_msgBox.setIcon(QMessageBox.Information)
        self.login_msgBox.setWindowTitle("登录成功！")
        self.login_msgBox.setText(
            f"{self.aurora_account_main.username} ({self.aurora_account_main.account_tier})已登录"
        )
        self.login_msgBox.exec_()

        self.login_window.close()
        BrokerWindow.aurora_account = self.aurora_account_main
        LevelOne.aurora_account = self.aurora_account_main
        LevelOne.server_ip = self.login_window.server_ip
        LevelOne.server_port = self.login_window.server_port
        LevelOne.token = self.token
        PositionSummary.aurora_account = self.aurora_account_main
        OrderDetails.aurora_account = self.aurora_account_main
        self.broker_window.show()
        self.broker_window.verify_local_broker_account()
        self.show()

    def on_sync_login_failed(self):
        QMessageBox.critical(self, "服务器异常", "请稍后再试")
        self.close_all_windows()
        self.close()

    def verified_broker_existed(self, broker_obj):
        self.broker_window.close()
        self.broker_list_main.append(broker_obj)
        self.reset_window()

    def open_broker(self):
        if self.aurora_account_main:
            self.broker_window.show()
        else:
            QMessageBox.critical(self, "打开窗口失败", "请登录")
            self.login_window.show()

    def open_level_one(self):
        if len(self.broker_list_main) > 0:
            logging.info("New level one window")
            logging.info(len(self.level_one_window_list))

            count = len(self.level_one_window_list)
            screensize = QApplication.primaryScreen().size()
            for level_one in reversed(self.level_one_window_list):
                try:
                    level_one.pos()
                except RuntimeError as e:
                    pass
                else:
                    y = level_one.pos().y() + 300
                    break
            for level_one in self.level_one_window_list:
                try:
                    level_one.pos()
                except RuntimeError as e:
                    # wrapped C/C++ object of type LevelOne has been deleted
                    count -= 1
                else:
                    pass
            if count == 0:
                y = 70
            if count > 17:
                QMessageBox.critical(self, "窗口数量过多", "请关闭部分Level One窗口")
                return
            if y + 300 > screensize.height():
                y = 70
            new_window = LevelOne()
            new_window.move(1210, y)
            self.level_one_window_list.append(new_window)
            new_window.show()
        else:
            QMessageBox.critical(self, "打开窗口失败", "请添加券商账户")

    # def open_level_two(self):
    #     if len(self.broker_list_main)>0:
    #         self.level_two_window_list.append(LevelTwo())
    #         self.level_two_window_list[-1].show()
    #     else:
    #         QMessageBox.critical(self, "Failed 打开窗口失败","请添加券商账户")

    def open_position_summary(self):
        if len(self.broker_list_main) > 0:
            self.position_summary_window.get_acc_pos()
            self.position_summary_window.show()
        else:
            QMessageBox.critical(self, "打开窗口失败", "请添加券商账户")

    def open_order_details(self):
        if len(self.broker_list_main) > 0:
            self.order_details_window.tab_changed()
            self.order_details_window.show()
        else:
            QMessageBox.critical(self, "打开窗口失败", "请添加券商账户")

    def reset_window(self):
        LevelOne.broker_list = self.broker_list_main
        # LevelTwo.broker_list = self.broker_list_main
        PositionSummary.broker_account_list = self.broker_list_main
        OrderDetails.broker_account_list = self.broker_list_main

        level_one_number = self.get_level_one_number()
        self.level_one_window_list.clear()
        if level_one_number:
            for i in range(level_one_number):
                self.level_one_window_list.append(LevelOne(layout_number=i))
            for level_one in self.level_one_window_list:
                level_one.show()
        else:
            self.level_one_window_list = [LevelOne()]
            self.level_one_window_list[0].show()

        # self.level_two_window_list = [LevelTwo()]
        self.position_summary_window = PositionSummary()
        self.position_summary_window.signal_window_failed.connect(self.on_window_failed)
        self.order_details_window = OrderDetails()
        self.order_details_window.signal_window_failed.connect(self.on_window_failed)

        # self.level_two_window_list[0].show()
        # self.position_summary_window.hide()
        # self.order_details_window.hide()

    def on_window_failed(self):
        QMessageBox.critical(self, "数据库更新/同步失败", "请检查网络后重启")
        self.close_all_windows()
        self.close()

    def close_all_windows(self):
        self.broker_window.close()
        if len(self.level_one_window_list) > 0:
            for level_one in self.level_one_window_list:
                try:
                    level_one.close()
                    for key, val in level_one.thread.items():
                        val.stop()
                except Exception as e:
                    # Level one will be deleted and ignored
                    # logging.error(str(e))
                    pass
        # for level_two in self.level_two_window_list:
        #     level_two.close()

        try:
            self.position_summary_window
        except AttributeError:
            pass
        else:

            for key, val in self.position_summary_window.thread.items():
                val.stop()
            # self.position_summary_window.thread[0].stop()
            self.position_summary_window.close()

        try:
            self.order_details_window
        except AttributeError:
            pass
        else:
            for key, val in self.order_details_window.thread.items():
                val.stop()
            # self.order_details_window.thread[3].stop()
            self.order_details_window.close()

    def delete_broker_account(self, deleted_acc):
        logging.info("deleting")
        for broker_acc in self.broker_list_main:
            if str(broker_acc) == str(deleted_acc):
                self.broker_list_main.remove(broker_acc)
                logging.info("deleted")
        if len(self.broker_list_main) > 0:
            self.reset_window()
        else:
            self.close_all_windows()

    def save_layout(self):

        layout_dict = {}

        try:
            self.broker_window
        except AttributeError:
            pass
        else:
            layout_dict["broker_window"] = {
                "x": self.broker_window.geometry().x(),
                "y": self.broker_window.geometry().y(),
                "w": self.broker_window.geometry().width(),
                "h": self.broker_window.geometry().height(),
            }

        if len(self.level_one_window_list) > 0:

            layout_dict["level_one_window"] = []
            for i, level_one in enumerate(self.level_one_window_list):
                try:
                    layout_dict["level_one_window"].append(
                        {
                            "x": level_one.geometry().x(),
                            "y": level_one.geometry().y(),
                            "w": level_one.geometry().width(),
                            "h": level_one.geometry().height(),
                        }
                    )
                except Exception as e:
                    pass

                # else:
                #     layout_dict["level_one_window"].append(
                #         {
                #             "x": level_one.geometry().x(),
                #             "y": level_one.geometry().y(),
                #             "w": level_one.geometry().width(),
                #             "h": level_one.geometry().height(),
                #         }
                #     )

            # try:
            #     self.level_one_window_list[0]
            #
            # except AttributeError:
            #     pass
            # else:
            #     layout_dict["level_one_window"] = {
            #         "x": self.level_one_window_list[0].geometry().x(),
            #         "y": self.level_one_window_list[0].geometry().y(),
            #         "w": self.level_one_window_list[0].geometry().width(),
            #         "h": self.level_one_window_list[0].geometry().height()
            #     }

        try:
            self.position_summary_window
        except AttributeError:
            pass
        else:
            layout_dict["position_summary_window"] = {
                "x": self.position_summary_window.geometry().x(),
                "y": self.position_summary_window.geometry().y(),
                "w": self.position_summary_window.geometry().width(),
                "h": self.position_summary_window.geometry().height(),
            }

        try:
            self.order_details_window
        except AttributeError:
            pass
        else:
            layout_dict["order_detail_window"] = {
                "x": self.order_details_window.geometry().x(),
                "y": self.order_details_window.geometry().y(),
                "w": self.order_details_window.geometry().width(),
                "h": self.order_details_window.geometry().height(),
            }

        try:
            file_path = r"temp/layout.json"
            with open(file_path, "w") as layoutF:
                json.dump(layout_dict, layoutF, separators=(",", ":"))

        except Exception as e:
            logging.error(str(e))
            QMessageBox.critical(self, "错误", "模板保存失败，请检查log.txt文件")

        else:
            QMessageBox.information(self, "成功", "模板已保存")

    def get_level_one_number(self):
        file_path = r"temp/layout.json"
        if os.path.exists(file_path) == False:
            return 0
        else:
            with open(file_path, "r") as layoutF:
                layout_obj = json.load(layoutF)
            if "level_one_window" in layout_obj:
                return len(layout_obj["level_one_window"])

    def minimize_sub_window(self):

        try:
            self.broker_window
        except AttributeError:
            pass
        else:
            if self.broker_window.isVisible():
                self.broker_window.showMinimized()

        if len(self.level_one_window_list) > 0:
            for level_one in self.level_one_window_list:
                try:
                    level_one.showMinimized()

                except Exception as e:
                    pass

        try:
            self.position_summary_window
        except AttributeError:
            pass
        else:
            self.position_summary_window.showMinimized()

        try:
            self.order_details_window
        except AttributeError:
            pass
        else:
            self.order_details_window.showMinimized()

    def normal_sub_window(self):
        try:
            self.broker_window
        except AttributeError:
            pass
        else:
            if self.broker_window.isVisible():
                self.broker_window.showNormal()

        if len(self.level_one_window_list) > 0:
            for level_one in self.level_one_window_list:
                try:
                    level_one.showNormal()

                except Exception as e:
                    pass

        try:
            self.position_summary_window
        except AttributeError:
            pass
        else:
            self.position_summary_window.showNormal()

        try:
            self.order_details_window
        except AttributeError:
            pass
        else:
            self.order_details_window.showNormal()

    def changeEvent(self, event) -> None:
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.minimize_sub_window()

            elif self.isActiveWindow():

                self.normal_sub_window()

    def closeEvent(self, event):
        result = QMessageBox.question(
            self,
            "确认",
            "是否确认退出?",
            QMessageBox.Yes | QMessageBox.No,
        )
        event.ignore()

        if result == QMessageBox.Yes:
            # os.system("rosnode kill -a")

            event.accept()
            try:
                self.thread[1].stop()
            except KeyError:
                pass
            try:
                self.thread[2].stop()
            except KeyError:
                pass
            self.close_all_windows()
            self.close()
            # sys.exit()


if __name__ == "__main__":
    # stylesheet = '''
    # QWidget{

    # }'''
    app = QApplication(sys.argv)
    mw = MainWindow()
    app.setStyleSheet("QMessageBox { messagebox-text-interaction-flags: 5; }")
    sys.exit(app.exec())
