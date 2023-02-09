import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LevelTwo(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(543, 810)
        self.verticalLayout_all = QVBoxLayout(self)
        self.verticalLayout_all.setObjectName(u"verticalLayout_all")
        # level_I data 部分
        # 布局
        self.widget_I = QWidget(self)
        self.widget_I.setObjectName(u"widget_I")
        self.widget_I.setGeometry(QRect(11, 65, 521, 22))
        self.horizontalLayout_I = QHBoxLayout(self.widget_I)
        self.horizontalLayout_I.setObjectName(u"horizontalLayout_I")
        self.horizontalLayout_I.setContentsMargins(0, 0, 0, 0)
        self.bidside_lineEdit = QLineEdit(self.widget_I)
        self.bidside_lineEdit.setObjectName(u"bidside_lineEdit")
        self.bidside_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_I.addWidget(self.bidside_lineEdit)

        self.bid_lineEdit = QLineEdit(self.widget_I)
        self.bid_lineEdit.setObjectName(u"bid_lineEdit")
        self.bid_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_I.addWidget(self.bid_lineEdit)

        self.last_lineEdit = QLineEdit(self.widget_I)
        self.last_lineEdit.setObjectName(u"last_lineEdit")
        self.last_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_I.addWidget(self.last_lineEdit)

        self.ask_lineEdit = QLineEdit(self.widget_I)
        self.ask_lineEdit.setObjectName(u"ask_lineEdit")
        self.ask_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_I.addWidget(self.ask_lineEdit)

        self.askside_lineEdit = QLineEdit(self.widget_I)
        self.askside_lineEdit.setObjectName(u"askside_lineEdit")
        self.askside_lineEdit.setAlignment(Qt.AlignCenter)
        self.horizontalLayout_I.addWidget(self.askside_lineEdit)

        # level I 信息栏显示为只读
        self.bidside_lineEdit.setReadOnly(True)
        self.bid_lineEdit.setReadOnly(True)
        self.last_lineEdit.setReadOnly(True)
        self.ask_lineEdit.setReadOnly(True)
        self.askside_lineEdit.setReadOnly(True)

        self.bidside_lineEdit.setText("15")

        # symbol 输入部分
        # 布局
        self.widget_sym = QWidget(self)
        self.widget_sym.setObjectName(u"widget_sym")
        self.widget_sym.setGeometry(QRect(12, 35, 183, 22))
        self.horizontalLayout_symbol = QHBoxLayout(self.widget_sym)
        self.horizontalLayout_symbol.setObjectName(u"horizontalLayout_symbol")
        self.horizontalLayout_symbol.setContentsMargins(0, 0, 0, 0)
        self.symbol_label = QLabel(self.widget_sym)
        self.symbol_label.setObjectName(u"symbol_label")
        self.symbol_label.setText(r"Symbol:")

        self.horizontalLayout_symbol.addWidget(self.symbol_label)

        self.symbol_lineEdit = QLineEdit(self.widget_sym)
        self.symbol_lineEdit.setObjectName(u"symbol_lineEdit")

        self.horizontalLayout_symbol.addWidget(self.symbol_lineEdit)

        self.horizontalLayout_symbol.addStretch(2)

        # level II data 部分
        # 布局
        self.widget_II = QWidget(self)
        self.widget_II.setObjectName(u"widget_II")
        self.widget_II.setGeometry(QRect(10, 100, 520, 471))
        self.horizontalLayout_II = QHBoxLayout(self.widget_II)
        self.horizontalLayout_II.setSpacing(0)
        self.horizontalLayout_II.setObjectName(u"horizontalLayout_II")
        self.horizontalLayout_II.setContentsMargins(0, 0, 0, 0)
        self.bid_tableView = QTableView(self.widget_II)
        self.bid_tableView.setObjectName(u"bid_tableView")

        self.horizontalLayout_II.addWidget(self.bid_tableView)

        self.ask_tableView = QTableView(self.widget_II)
        self.ask_tableView.setObjectName(u"ask_tableView")

        self.horizontalLayout_II.addWidget(self.ask_tableView)

        # tableview 设置
        self.bid_model = QStandardItemModel(20, 3)
        self.bid_model.setHorizontalHeaderLabels(["Maker", "Price", "Size"])
        self.ask_model = QStandardItemModel(20, 3)
        self.ask_model.setHorizontalHeaderLabels(["Maker", "Price", "Size"])

        # 不显示索引列
        self.bid_tableView.verticalHeader().setVisible(False)
        self.ask_tableView.verticalHeader().setVisible(False)

        # 无网格
        self.bid_tableView.setShowGrid(False)
        self.ask_tableView.setShowGrid(False)

        # 设置表格为自适应的伸缩模式，即可根据窗口的大小来改变网格的大小
        self.bid_tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ask_tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 将表格变为禁止编辑
        self.bid_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ask_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 数据， 后期需要券商接口来设计数据的添加逻辑
        bid_item01 = QStandardItem("NASD")
        bid_item02 = QStandardItem("10.52")
        bid_item03 = QStandardItem("5")

        bid_item11 = QStandardItem("ARCA")
        bid_item12 = QStandardItem("10.52")
        bid_item13 = QStandardItem("10")

        bid_item21 = QStandardItem("BATS")
        bid_item22 = QStandardItem("10.51")
        bid_item23 = QStandardItem("8")

        bid_item31 = QStandardItem("NASD")
        bid_item32 = QStandardItem("10.50")
        bid_item33 = QStandardItem("20")

        bid_item41 = QStandardItem("ARCA")
        bid_item42 = QStandardItem("10.50")
        bid_item43 = QStandardItem("15")

        bid_item51 = QStandardItem("EDGX")
        bid_item52 = QStandardItem("10.48")
        bid_item53 = QStandardItem("3")

        ask_item01 = QStandardItem("ARCA")
        ask_item02 = QStandardItem("10.58")
        ask_item03 = QStandardItem("15")

        # 字体居中
        bid_item01.setTextAlignment(Qt.AlignCenter)
        bid_item02.setTextAlignment(Qt.AlignCenter)
        bid_item03.setTextAlignment(Qt.AlignCenter)

        bid_item11.setTextAlignment(Qt.AlignCenter)
        bid_item12.setTextAlignment(Qt.AlignCenter)
        bid_item13.setTextAlignment(Qt.AlignCenter)

        bid_item21.setTextAlignment(Qt.AlignCenter)
        bid_item22.setTextAlignment(Qt.AlignCenter)
        bid_item23.setTextAlignment(Qt.AlignCenter)

        bid_item31.setTextAlignment(Qt.AlignCenter)
        bid_item32.setTextAlignment(Qt.AlignCenter)
        bid_item33.setTextAlignment(Qt.AlignCenter)

        bid_item41.setTextAlignment(Qt.AlignCenter)
        bid_item42.setTextAlignment(Qt.AlignCenter)
        bid_item43.setTextAlignment(Qt.AlignCenter)

        bid_item51.setTextAlignment(Qt.AlignCenter)
        bid_item52.setTextAlignment(Qt.AlignCenter)
        bid_item53.setTextAlignment(Qt.AlignCenter)

        ask_item01.setTextAlignment(Qt.AlignCenter)
        ask_item02.setTextAlignment(Qt.AlignCenter)
        ask_item03.setTextAlignment(Qt.AlignCenter)

        # 背景颜色
        bid_item01.setBackground(QBrush(QColor(255, 255, 96)))
        bid_item02.setBackground(bid_item01.background())
        bid_item03.setBackground(bid_item01.background())

        bid_item11.setBackground(QBrush(QColor(255, 255, 96)))
        bid_item12.setBackground(bid_item11.background())
        bid_item13.setBackground(bid_item11.background())

        bid_item21.setBackground(QBrush(QColor(96, 255, 96)))
        bid_item22.setBackground(bid_item21.background())
        bid_item23.setBackground(bid_item21.background())

        bid_item31.setBackground(QBrush(QColor(128, 255, 255)))
        bid_item32.setBackground(bid_item31.background())
        bid_item33.setBackground(bid_item31.background())

        bid_item41.setBackground(QBrush(QColor(128, 255, 255)))
        bid_item42.setBackground(bid_item41.background())
        bid_item43.setBackground(bid_item41.background())

        bid_item51.setBackground(QBrush(QColor(255, 96, 96)))
        bid_item52.setBackground(bid_item51.background())
        bid_item53.setBackground(bid_item51.background())

        # 添加数据
        self.bid_model.setItem(0, 0, bid_item01)
        self.bid_model.setItem(0, 1, bid_item02)
        self.bid_model.setItem(0, 2, bid_item03)

        self.bid_model.setItem(1, 0, bid_item11)
        self.bid_model.setItem(1, 1, bid_item12)
        self.bid_model.setItem(1, 2, bid_item13)

        self.bid_model.setItem(2, 0, bid_item21)
        self.bid_model.setItem(2, 1, bid_item22)
        self.bid_model.setItem(2, 2, bid_item23)

        self.bid_model.setItem(3, 0, bid_item31)
        self.bid_model.setItem(3, 1, bid_item32)
        self.bid_model.setItem(3, 2, bid_item33)

        self.bid_model.setItem(4, 0, bid_item41)
        self.bid_model.setItem(4, 1, bid_item42)
        self.bid_model.setItem(4, 2, bid_item43)

        self.bid_model.setItem(5, 0, bid_item51)
        self.bid_model.setItem(5, 1, bid_item52)
        self.bid_model.setItem(5, 2, bid_item53)

        self.ask_model.setItem(0, 0, ask_item01)
        self.ask_model.setItem(0, 1, ask_item02)
        self.ask_model.setItem(0, 2, ask_item03)

        # 关联QTableView控件和Model
        self.bid_tableView.setModel(self.bid_model)
        self.ask_tableView.setModel(self.ask_model)

        # 自定义 menu_bar
        self.myQMenuBar = QMenuBar(self)
        self.myQMenuBar.addMenu("Actions")
        self.settings = self.myQMenuBar.addMenu("View")

        test1_act = QAction("change", self)
        self.settings.addAction(test1_act)
        test1_act.triggered.connect(self.change_bid_side)

        # 自定义 status_bar
        self.widget_status = QWidget(self)
        self.widget_status.setObjectName(u"widget_status")
        self.widget_status.setGeometry(QRect(0, 0, 540, 1180))
        self.statuslayout = QHBoxLayout(self.widget_status)
        self.statuslayout.setContentsMargins(0, 0, 0, 0)

        self.myStatusBar = QStatusBar(self.widget_status)
        self.myStatusBar.addWidget(QLabel("1"), 1)
        self.myStatusBar.addWidget(QLabel("2"), 1)
        self.myStatusBar.addWidget(QLineEdit(), 2)

        self.statuslayout.addWidget(self.myStatusBar)

        # 相对布局
        self.verticalLayout_all.addWidget(self.myQMenuBar)
        self.verticalLayout_all.addWidget(self.widget_sym)
        self.verticalLayout_all.addWidget(self.widget_I)
        self.verticalLayout_all.addWidget(self.widget_II)
        self.verticalLayout_all.addWidget(self.widget_status)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def change_bid_side(self):
        self.bidside_lineEdit.setText("20")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    level_two = LevelTwo()
    level_two.show()
    sys.exit(app.exec_())