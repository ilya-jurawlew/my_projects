# -*- coding: utf-8 -*-

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.message_box = QPlainTextEdit(self.centralwidget)
        self.message_box.setObjectName(u"message_box")
        self.message_box.setGeometry(QRect(10, 10, 321, 521))
        self.message_box.setReadOnly(True)

        self.message_input = QLineEdit(self.centralwidget)
        self.message_input.setObjectName(u"message_input")
        self.message_input.setGeometry(QRect(10, 540, 321, 20))

        self.message_button = QPushButton(self.centralwidget)
        self.message_button.setObjectName(u"message_button")
        self.message_button.setGeometry(QRect(10, 570, 321, 23))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.message_box.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Connecting", None))
        self.message_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type message", None))
        self.message_button.setText(QCoreApplication.translate("MainWindow", u"Send", None))
