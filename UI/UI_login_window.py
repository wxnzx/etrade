# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_login_window.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(791, 434)
        widget.setMouseTracking(False)
        widget.setStyleSheet("")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(widget)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(458, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMaximumSize(QtCore.QSize(139, 68))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/images/aurora_logo_only.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.label_7 = QtWidgets.QLabel(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        self.label_7.setMaximumSize(QtCore.QSize(244, 68))
        self.label_7.setAutoFillBackground(False)
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap(":/images/aurora_name_only.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(458, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(widget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.username_edit = QtWidgets.QLineEdit(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.username_edit.sizePolicy().hasHeightForWidth())
        self.username_edit.setSizePolicy(sizePolicy)
        self.username_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.username_edit.setObjectName("username_edit")
        self.horizontalLayout_5.addWidget(self.username_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.password_edit = QtWidgets.QLineEdit(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_edit.sizePolicy().hasHeightForWidth())
        self.password_edit.setSizePolicy(sizePolicy)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.password_edit.setObjectName("password_edit")
        self.horizontalLayout_7.addWidget(self.password_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        spacerItem5 = QtWidgets.QSpacerItem(458, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.legalese_checkBox = QtWidgets.QCheckBox(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.legalese_checkBox.sizePolicy().hasHeightForWidth())
        self.legalese_checkBox.setSizePolicy(sizePolicy)
        self.legalese_checkBox.setText("")
        self.legalese_checkBox.setTristate(False)
        self.legalese_checkBox.setObjectName("legalese_checkBox")
        self.horizontalLayout_2.addWidget(self.legalese_checkBox)
        self.legalese_label = QtWidgets.QLabel(widget)
        self.legalese_label.setObjectName("legalese_label")
        self.horizontalLayout_2.addWidget(self.legalese_label)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem8 = QtWidgets.QSpacerItem(458, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.submit_button = QtWidgets.QPushButton(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit_button.sizePolicy().hasHeightForWidth())
        self.submit_button.setSizePolicy(sizePolicy)
        self.submit_button.setFlat(False)
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout_4.addWidget(self.submit_button)
        self.settings_button = QtWidgets.QPushButton(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(sizePolicy)
        self.settings_button.setCheckable(False)
        self.settings_button.setAutoDefault(False)
        self.settings_button.setDefault(False)
        self.settings_button.setFlat(False)
        self.settings_button.setObjectName("settings_button")
        self.horizontalLayout_4.addWidget(self.settings_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.textBrowser = QtWidgets.QTextBrowser(widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.horizontalLayout_10.addLayout(self.verticalLayout_3)
        self.settings_group = QtWidgets.QGroupBox(widget)
        self.settings_group.setFlat(False)
        self.settings_group.setCheckable(False)
        self.settings_group.setObjectName("settings_group")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.settings_group)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_8 = QtWidgets.QLabel(self.settings_group)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.lineEdit_hostname = QtWidgets.QLineEdit(self.settings_group)
        self.lineEdit_hostname.setObjectName("lineEdit_hostname")
        self.verticalLayout_2.addWidget(self.lineEdit_hostname)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter)
        self.checkBox = QtWidgets.QCheckBox(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_6.addWidget(self.checkBox)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.lineEdit_ip = QtWidgets.QLineEdit(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_ip.sizePolicy().hasHeightForWidth())
        self.lineEdit_ip.setSizePolicy(sizePolicy)
        self.lineEdit_ip.setText("")
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.verticalLayout_2.addWidget(self.lineEdit_ip)
        self.label_6 = QtWidgets.QLabel(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.spinBox_port = QtWidgets.QSpinBox(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_port.sizePolicy().hasHeightForWidth())
        self.spinBox_port.setSizePolicy(sizePolicy)
        self.spinBox_port.setMaximum(65525)
        self.spinBox_port.setProperty("value", 8888)
        self.spinBox_port.setObjectName("spinBox_port")
        self.horizontalLayout_9.addWidget(self.spinBox_port)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.settings_submit_button = QtWidgets.QPushButton(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_submit_button.sizePolicy().hasHeightForWidth())
        self.settings_submit_button.setSizePolicy(sizePolicy)
        self.settings_submit_button.setObjectName("settings_submit_button")
        self.horizontalLayout_3.addWidget(self.settings_submit_button)
        self.settings_reset_button = QtWidgets.QPushButton(self.settings_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settings_reset_button.sizePolicy().hasHeightForWidth())
        self.settings_reset_button.setSizePolicy(sizePolicy)
        self.settings_reset_button.setObjectName("settings_reset_button")
        self.horizontalLayout_3.addWidget(self.settings_reset_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_9 = QtWidgets.QLabel(self.settings_group)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem11)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_10.addWidget(self.settings_group)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Login"))
        self.label.setText(_translate("widget", "<html><head/><body><p align=\"center\"><span style=\"font-size:28pt; color:#2B1C5C;font-family: Papyrus\">POLARIS</span></p></body></html>"))
        self.label_2.setText(_translate("widget", "用户名"))
        self.label_3.setText(_translate("widget", "密码"))
        self.legalese_label.setText(_translate("widget", "<html><head/><body><p>同意并遵守<a href=\"https://www.auroraclearing.net/terms\"><span style=\" text-decoration: underline; color:#0000ff;\">服务条款</span></a></p></body></html>"))
        self.submit_button.setText(_translate("widget", "登录"))
        self.settings_button.setText(_translate("widget", "设置"))
        self.settings_group.setTitle(_translate("widget", "设置"))
        self.label_8.setText(_translate("widget", "服务器Hostname："))
        self.label_5.setText(_translate("widget", "服务器IP："))
        self.checkBox.setText(_translate("widget", "手动设置"))
        self.label_6.setText(_translate("widget", "服务器端口："))
        self.settings_submit_button.setText(_translate("widget", "提交"))
        self.settings_reset_button.setText(_translate("widget", "重置"))
        self.label_9.setText(_translate("widget", "<html><head/><body><p>备注： </p><p>1. 如需更改设置，请在更改后点击提交。</p><p>2. 设置服务器Hostname后可自动获取服务器IP。</p><p>3. 如需手动设置IP，请咨询Aurora Polaris团队。</p></body></html>"))

import img.img_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

