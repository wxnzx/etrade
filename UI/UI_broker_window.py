# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_broker_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(967, 897)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.groupBox_add = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_add.sizePolicy().hasHeightForWidth())
        self.groupBox_add.setSizePolicy(sizePolicy)
        self.groupBox_add.setObjectName("groupBox_add")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_add)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.groupBox_add)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.broker_comboBox = QtWidgets.QComboBox(self.groupBox_add)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.broker_comboBox.sizePolicy().hasHeightForWidth())
        self.broker_comboBox.setSizePolicy(sizePolicy)
        self.broker_comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.broker_comboBox.setObjectName("broker_comboBox")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.setItemText(0, "")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.broker_comboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.broker_comboBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.tabWidget = QtWidgets.QTabWidget(self.groupBox_add)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.futu_host_edit = QtWidgets.QLineEdit(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.futu_host_edit.sizePolicy().hasHeightForWidth())
        self.futu_host_edit.setSizePolicy(sizePolicy)
        self.futu_host_edit.setObjectName("futu_host_edit")
        self.gridLayout.addWidget(self.futu_host_edit, 0, 1, 1, 1)
        self.futu_port_spin = QtWidgets.QSpinBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.futu_port_spin.sizePolicy().hasHeightForWidth())
        self.futu_port_spin.setSizePolicy(sizePolicy)
        self.futu_port_spin.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.futu_port_spin.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.futu_port_spin.setMaximum(62255)
        self.futu_port_spin.setProperty("value", 11111)
        self.futu_port_spin.setObjectName("futu_port_spin")
        self.gridLayout.addWidget(self.futu_port_spin, 1, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.futu_disclaimer_check = QtWidgets.QCheckBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.futu_disclaimer_check.sizePolicy().hasHeightForWidth())
        self.futu_disclaimer_check.setSizePolicy(sizePolicy)
        self.futu_disclaimer_check.setText("")
        self.futu_disclaimer_check.setObjectName("futu_disclaimer_check")
        self.horizontalLayout_9.addWidget(self.futu_disclaimer_check, 0, QtCore.Qt.AlignHCenter)
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_9.addWidget(self.label_12, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_6.addLayout(self.horizontalLayout_9)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem1)
        self.horizontalLayout_12.addLayout(self.verticalLayout_6)
        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem2)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_15 = QtWidgets.QLabel(self.tab_4)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_21.addWidget(self.label_15, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_tigerId = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_tigerId.sizePolicy().hasHeightForWidth())
        self.lineEdit_tigerId.setSizePolicy(sizePolicy)
        self.lineEdit_tigerId.setObjectName("lineEdit_tigerId")
        self.horizontalLayout_21.addWidget(self.lineEdit_tigerId)
        self.verticalLayout_13.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.label_16 = QtWidgets.QLabel(self.tab_4)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_22.addWidget(self.label_16, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_tigerAcc = QtWidgets.QLineEdit(self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_tigerAcc.sizePolicy().hasHeightForWidth())
        self.lineEdit_tigerAcc.setSizePolicy(sizePolicy)
        self.lineEdit_tigerAcc.setObjectName("lineEdit_tigerAcc")
        self.horizontalLayout_22.addWidget(self.lineEdit_tigerAcc)
        self.verticalLayout_13.addLayout(self.horizontalLayout_22)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_17 = QtWidgets.QLabel(self.tab_4)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_12.addWidget(self.label_17, 0, QtCore.Qt.AlignHCenter)
        self.textEdit_tigerKey = QtWidgets.QTextEdit(self.tab_4)
        self.textEdit_tigerKey.setObjectName("textEdit_tigerKey")
        self.verticalLayout_12.addWidget(self.textEdit_tigerKey)
        self.verticalLayout_13.addLayout(self.verticalLayout_12)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_13.addItem(spacerItem3)
        self.horizontalLayout_23.addLayout(self.verticalLayout_13)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_clientID = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_clientID.sizePolicy().hasHeightForWidth())
        self.lineEdit_clientID.setSizePolicy(sizePolicy)
        self.lineEdit_clientID.setObjectName("lineEdit_clientID")
        self.horizontalLayout_3.addWidget(self.lineEdit_clientID)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_17.addWidget(self.label_13, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_redirect_uri = QtWidgets.QLineEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_redirect_uri.sizePolicy().hasHeightForWidth())
        self.lineEdit_redirect_uri.setSizePolicy(sizePolicy)
        self.lineEdit_redirect_uri.setObjectName("lineEdit_redirect_uri")
        self.horizontalLayout_17.addWidget(self.lineEdit_redirect_uri)
        self.verticalLayout.addLayout(self.horizontalLayout_17)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3, 0, QtCore.Qt.AlignHCenter)
        self.textEdit_refreshToken = QtWidgets.QTextEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_refreshToken.sizePolicy().hasHeightForWidth())
        self.textEdit_refreshToken.setSizePolicy(sizePolicy)
        self.textEdit_refreshToken.setObjectName("textEdit_refreshToken")
        self.verticalLayout.addWidget(self.textEdit_refreshToken)
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.pushButton_generateToken = QtWidgets.QPushButton(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_generateToken.sizePolicy().hasHeightForWidth())
        self.pushButton_generateToken.setSizePolicy(sizePolicy)
        self.pushButton_generateToken.setObjectName("pushButton_generateToken")
        self.verticalLayout.addWidget(self.pushButton_generateToken, 0, QtCore.Qt.AlignHCenter)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_14.addLayout(self.verticalLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem5)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_4 = QtWidgets.QLabel(self.tab_3)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_username = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_username.sizePolicy().hasHeightForWidth())
        self.lineEdit_username.setSizePolicy(sizePolicy)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.horizontalLayout_10.addWidget(self.lineEdit_username)
        self.verticalLayout_10.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_11.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_password = QtWidgets.QLineEdit(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_password.sizePolicy().hasHeightForWidth())
        self.lineEdit_password.setSizePolicy(sizePolicy)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.horizontalLayout_11.addWidget(self.lineEdit_password)
        self.verticalLayout_10.addLayout(self.horizontalLayout_11)
        self.verticalLayout_11.addLayout(self.verticalLayout_10)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem6)
        self.horizontalLayout_18.addLayout(self.verticalLayout_11)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.tab_6)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout()
        self.verticalLayout_16.setContentsMargins(20, -1, 20, -1)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_16.addItem(spacerItem7)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_18 = QtWidgets.QLabel(self.tab_6)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_24.addWidget(self.label_18, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_userEtrade = QtWidgets.QLineEdit(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_userEtrade.sizePolicy().hasHeightForWidth())
        self.lineEdit_userEtrade.setSizePolicy(sizePolicy)
        self.lineEdit_userEtrade.setObjectName("lineEdit_userEtrade")
        self.horizontalLayout_24.addWidget(self.lineEdit_userEtrade)
        self.verticalLayout_16.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_19 = QtWidgets.QLabel(self.tab_6)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_25.addWidget(self.label_19, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit_passEtrade = QtWidgets.QLineEdit(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_passEtrade.sizePolicy().hasHeightForWidth())
        self.lineEdit_passEtrade.setSizePolicy(sizePolicy)
        self.lineEdit_passEtrade.setObjectName("lineEdit_passEtrade")
        self.horizontalLayout_25.addWidget(self.lineEdit_passEtrade)
        self.verticalLayout_16.addLayout(self.horizontalLayout_25)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_20 = QtWidgets.QLabel(self.tab_6)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_14.addWidget(self.label_20, 0, QtCore.Qt.AlignHCenter)
        self.textEdit_key = QtWidgets.QTextEdit(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_key.sizePolicy().hasHeightForWidth())
        self.textEdit_key.setSizePolicy(sizePolicy)
        self.textEdit_key.setObjectName("textEdit_key")
        self.verticalLayout_14.addWidget(self.textEdit_key)
        self.verticalLayout_16.addLayout(self.verticalLayout_14)
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_21 = QtWidgets.QLabel(self.tab_6)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_15.addWidget(self.label_21, 0, QtCore.Qt.AlignHCenter)
        self.textEdit_secret = QtWidgets.QTextEdit(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_secret.sizePolicy().hasHeightForWidth())
        self.textEdit_secret.setSizePolicy(sizePolicy)
        self.textEdit_secret.setObjectName("textEdit_secret")
        self.verticalLayout_15.addWidget(self.textEdit_secret)
        self.verticalLayout_16.addLayout(self.verticalLayout_15)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_16.addItem(spacerItem8)
        self.horizontalLayout_26.addLayout(self.verticalLayout_16)
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.tabWidget.addTab(self.tab_7, "")
        self.verticalLayout_5.addWidget(self.tabWidget)
        self.groupBox_getAccList = QtWidgets.QGroupBox(self.groupBox_add)
        self.groupBox_getAccList.setTitle("")
        self.groupBox_getAccList.setObjectName("groupBox_getAccList")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.groupBox_getAccList)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.pushButton_getAccList = QtWidgets.QPushButton(self.groupBox_getAccList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_getAccList.sizePolicy().hasHeightForWidth())
        self.pushButton_getAccList.setSizePolicy(sizePolicy)
        self.pushButton_getAccList.setObjectName("pushButton_getAccList")
        self.horizontalLayout_16.addWidget(self.pushButton_getAccList)
        self.verticalLayout_5.addWidget(self.groupBox_getAccList)
        self.groupBox_accList = QtWidgets.QGroupBox(self.groupBox_add)
        self.groupBox_accList.setTitle("")
        self.groupBox_accList.setObjectName("groupBox_accList")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_accList)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_11 = QtWidgets.QLabel(self.groupBox_accList)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_8.addWidget(self.label_11)
        self.tableView_accList = QtWidgets.QTableView(self.groupBox_accList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_accList.sizePolicy().hasHeightForWidth())
        self.tableView_accList.setSizePolicy(sizePolicy)
        self.tableView_accList.setObjectName("tableView_accList")
        self.verticalLayout_8.addWidget(self.tableView_accList)
        self.horizontalLayout_8.addLayout(self.verticalLayout_8)
        self.verticalLayout_5.addWidget(self.groupBox_accList)
        self.groupBox_tp = QtWidgets.QGroupBox(self.groupBox_add)
        self.groupBox_tp.setTitle("")
        self.groupBox_tp.setObjectName("groupBox_tp")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.groupBox_tp)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem9)
        self.label_5 = QtWidgets.QLabel(self.groupBox_tp)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.trading_password_edit = QtWidgets.QLineEdit(self.groupBox_tp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trading_password_edit.sizePolicy().hasHeightForWidth())
        self.trading_password_edit.setSizePolicy(sizePolicy)
        self.trading_password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.trading_password_edit.setObjectName("trading_password_edit")
        self.horizontalLayout_5.addWidget(self.trading_password_edit)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem10)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_5)
        self.verticalLayout_5.addWidget(self.groupBox_tp)
        self.add_broker_button = QtWidgets.QPushButton(self.groupBox_add)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_broker_button.sizePolicy().hasHeightForWidth())
        self.add_broker_button.setSizePolicy(sizePolicy)
        self.add_broker_button.setDefault(True)
        self.add_broker_button.setFlat(False)
        self.add_broker_button.setObjectName("add_broker_button")
        self.verticalLayout_5.addWidget(self.add_broker_button, 0, QtCore.Qt.AlignHCenter)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem11)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem12)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        self.horizontalLayout_19.addWidget(self.groupBox_add)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_19.addWidget(self.line)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_verify = QtWidgets.QGroupBox(Form)
        self.groupBox_verify.setObjectName("groupBox_verify")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_verify)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.broker_table_view = QtWidgets.QTableView(self.groupBox_verify)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.broker_table_view.sizePolicy().hasHeightForWidth())
        self.broker_table_view.setSizePolicy(sizePolicy)
        self.broker_table_view.setObjectName("broker_table_view")
        self.horizontalLayout.addWidget(self.broker_table_view)
        self.verticalLayout_2.addWidget(self.groupBox_verify)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem13)
        self.groupBox_delete = QtWidgets.QGroupBox(Form)
        self.groupBox_delete.setObjectName("groupBox_delete")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.groupBox_delete)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_8 = QtWidgets.QLabel(self.groupBox_delete)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.id_edit = QtWidgets.QLineEdit(self.groupBox_delete)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.id_edit.sizePolicy().hasHeightForWidth())
        self.id_edit.setSizePolicy(sizePolicy)
        self.id_edit.setObjectName("id_edit")
        self.horizontalLayout_2.addWidget(self.id_edit)
        self.delete_button = QtWidgets.QPushButton(self.groupBox_delete)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_button.sizePolicy().hasHeightForWidth())
        self.delete_button.setSizePolicy(sizePolicy)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_2.addWidget(self.delete_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_9.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.line_4 = QtWidgets.QFrame(self.groupBox_delete)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_4.addWidget(self.line_4)
        self.label_7 = QtWidgets.QLabel(self.groupBox_delete)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.delete_local_button = QtWidgets.QPushButton(self.groupBox_delete)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_local_button.sizePolicy().hasHeightForWidth())
        self.delete_local_button.setSizePolicy(sizePolicy)
        self.delete_local_button.setObjectName("delete_local_button")
        self.verticalLayout_4.addWidget(self.delete_local_button, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_9.addLayout(self.verticalLayout_4)
        self.horizontalLayout_13.addLayout(self.verticalLayout_9)
        self.verticalLayout_2.addWidget(self.groupBox_delete)
        self.horizontalLayout_19.addLayout(self.verticalLayout_2)
        self.horizontalLayout_20.addLayout(self.horizontalLayout_19)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Broker Accounts"))
        self.groupBox_add.setTitle(_translate("Form", "添加新的账户"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">请选择券商:</p></body></html>"))
        self.broker_comboBox.setItemText(1, _translate("Form", "FUTUBULL 富途牛牛"))
        self.broker_comboBox.setItemText(2, _translate("Form", "FUTU MOOMOO"))
        self.broker_comboBox.setItemText(3, _translate("Form", "TIGER 老虎证券"))
        self.broker_comboBox.setItemText(4, _translate("Form", "TD Ameritrade"))
        self.broker_comboBox.setItemText(5, _translate("Form", "Interactive Brokers"))
        self.broker_comboBox.setItemText(6, _translate("Form", "E*Trade"))
        self.broker_comboBox.setItemText(7, _translate("Form", "Tradier"))
        self.broker_comboBox.setItemText(8, _translate("Form", "BLACKBULL Trade"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "Page"))
        self.futu_host_edit.setText(_translate("Form", "127.0.0.1"))
        self.label_10.setText(_translate("Form", "FutuOpenD PORT"))
        self.label_9.setText(_translate("Form", "FutuOpenD HOST"))
        self.label_12.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">请在使用本系统前登录FutuOpenD网关</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">并完成API免责条款。</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "futu"))
        self.label_15.setText(_translate("Form", "Tiger ID"))
        self.label_16.setText(_translate("Form", "Account Number"))
        self.label_17.setText(_translate("Form", "Private Key"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "tiger"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p>Client ID</p></body></html>"))
        self.label_13.setText(_translate("Form", "Callback URL"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p align=\"center\">Refresh Token</p></body></html>"))
        self.label_14.setText(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; color:#aa0000;\">如果您没有Refresh Token，请点击生成Refresh Token按钮生成</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; color:#aa0000;\">请将生成的Refresn Token复制并保存</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; color:#aa0000;\">每个Refresh Token有效期为90天</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; color:#aa0000;\">请避免频繁生成新的Refresh Token，否则将需等待API解封</span></p></body></html>"))
        self.pushButton_generateToken.setText(_translate("Form", "生成Refresh Token"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "td"))
        self.label_4.setText(_translate("Form", "Username"))
        self.label_6.setText(_translate("Form", "Password"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "ib"))
        self.label_18.setText(_translate("Form", "Username"))
        self.label_19.setText(_translate("Form", "Password"))
        self.label_20.setText(_translate("Form", "Consumer Key"))
        self.label_21.setText(_translate("Form", "Consumer Secret"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Form", "etrade"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Form", "tradier"))
        self.pushButton_getAccList.setText(_translate("Form", "获取账户列表"))
        self.label_11.setText(_translate("Form", "<html><head/><body><p align=\"center\">请选择一个账户添加</p></body></html>"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p>交易密码</p></body></html>"))
        self.add_broker_button.setText(_translate("Form", "添加账户"))
        self.groupBox_verify.setTitle(_translate("Form", "已验证登录的账户"))
        self.groupBox_delete.setTitle(_translate("Form", "删除验证登录账户"))
        self.label_8.setText(_translate("Form", "<html><head/><body><p align=\"center\">请输入列表中的ID来删除</p></body></html>"))
        self.delete_button.setText(_translate("Form", "删除"))
        self.label_7.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" color:#d0021b;\">删除所有账户</span></p></body></html>"))
        self.delete_local_button.setText(_translate("Form", "删除全部"))
