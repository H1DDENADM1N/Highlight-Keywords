# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'highlight_keywords.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 300)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_select_file = QPushButton(Form)
        self.pushButton_select_file.setObjectName(u"pushButton_select_file")

        self.horizontalLayout.addWidget(self.pushButton_select_file)

        self.pushButton_select_folder = QPushButton(Form)
        self.pushButton_select_folder.setObjectName(u"pushButton_select_folder")

        self.horizontalLayout.addWidget(self.pushButton_select_folder)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_selected_path = QLabel(Form)
        self.label_selected_path.setObjectName(u"label_selected_path")

        self.verticalLayout.addWidget(self.label_selected_path)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_strategy = QLabel(Form)
        self.label_strategy.setObjectName(u"label_strategy")

        self.horizontalLayout_2.addWidget(self.label_strategy)

        self.comboBox_strategy = QComboBox(Form)
        self.comboBox_strategy.addItem("")
        self.comboBox_strategy.addItem("")
        self.comboBox_strategy.addItem("")
        self.comboBox_strategy.setObjectName(u"comboBox_strategy")

        self.horizontalLayout_2.addWidget(self.comboBox_strategy)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_edit_keywords = QPushButton(Form)
        self.pushButton_edit_keywords.setObjectName(u"pushButton_edit_keywords")

        self.horizontalLayout_3.addWidget(self.pushButton_edit_keywords)

        self.pushButton_execute = QPushButton(Form)
        self.pushButton_execute.setObjectName(u"pushButton_execute")
        self.pushButton_execute.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.pushButton_execute)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_info = QLabel(Form)
        self.label_info.setObjectName(u"label_info")

        self.verticalLayout_2.addWidget(self.label_info)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"HIGHTLIGHT KEYWORDS", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("Form", u"\u9009\u62e9 \u6587\u4ef6", None))
        self.pushButton_select_folder.setText(QCoreApplication.translate("Form", u"\u9009\u62e9 \u6587\u4ef6\u5939", None))
        self.label_selected_path.setText(QCoreApplication.translate("Form", u"\u5df2\u9009\u62e9\uff1a", None))
        self.label_strategy.setText(QCoreApplication.translate("Form", u"\u9ad8\u4eae\u7b56\u7565\uff1a", None))
        self.comboBox_strategy.setItemText(0, QCoreApplication.translate("Form", u"1. Markdown", None))
        self.comboBox_strategy.setItemText(1, QCoreApplication.translate("Form", u"2. Text", None))
        self.comboBox_strategy.setItemText(2, QCoreApplication.translate("Form", u"3. HTML", None))

        self.pushButton_edit_keywords.setText(QCoreApplication.translate("Form", u"\u7f16\u8f91 \u9ad8\u4eae\u5173\u952e\u5b57", None))
        self.pushButton_execute.setText(QCoreApplication.translate("Form", u"\u6267\u884c", None))
        self.label_info.setText(QCoreApplication.translate("Form", u"\u4fe1\u606f\uff1a", None))
    # retranslateUi

