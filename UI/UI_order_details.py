# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_order_details_new.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1240, 335)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_acc = QtWidgets.QLabel(Form)
        self.label_acc.setObjectName("label_acc")
        self.verticalLayout.addWidget(self.label_acc)
        self.listWidget_acc = QtWidgets.QListWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_acc.sizePolicy().hasHeightForWidth())
        self.listWidget_acc.setSizePolicy(sizePolicy)
        self.listWidget_acc.setObjectName("listWidget_acc")
        self.verticalLayout.addWidget(self.listWidget_acc)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_CM = QtWidgets.QLabel(Form)
        self.label_CM.setObjectName("label_CM")
        self.verticalLayout_7.addWidget(self.label_CM)
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_7.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout_7)
        self.groupBox_fitler = QtWidgets.QGroupBox(Form)
        self.groupBox_fitler.setObjectName("groupBox_fitler")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.groupBox_fitler)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.dateEdit_from = QtWidgets.QDateEdit(self.groupBox_fitler)
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_from.setObjectName("dateEdit_from")
        self.horizontalLayout_13.addWidget(self.dateEdit_from)
        self.dateEdit_to = QtWidgets.QDateEdit(self.groupBox_fitler)
        self.dateEdit_to.setCalendarPopup(True)
        self.dateEdit_to.setObjectName("dateEdit_to")
        self.horizontalLayout_13.addWidget(self.dateEdit_to)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_13)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_12)
        self.verticalLayout_2.addWidget(self.groupBox_fitler)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Order Details"))
        self.label_acc.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">双击选择一个账户显示</span></p></body></html>"))
        self.label_CM.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">双击取消或修改订单</span></p></body></html>"))
        self.groupBox_fitler.setTitle(_translate("Form", "历史筛选"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

