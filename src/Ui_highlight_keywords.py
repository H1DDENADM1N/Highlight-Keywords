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
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(507, 348)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
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


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_selected_path = QLabel(Form)
        self.label_selected_path.setObjectName(u"label_selected_path")

        self.verticalLayout_3.addWidget(self.label_selected_path)

        self.plainTextEdit_selected_path = QPlainTextEdit(Form)
        self.plainTextEdit_selected_path.setObjectName(u"plainTextEdit_selected_path")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit_selected_path.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_selected_path.setSizePolicy(sizePolicy)
        self.plainTextEdit_selected_path.setMinimumSize(QSize(0, 50))
        self.plainTextEdit_selected_path.setMaximumSize(QSize(16777215, 16777215))
        self.plainTextEdit_selected_path.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit_selected_path)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

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


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_edit_keywords = QPushButton(Form)
        self.pushButton_edit_keywords.setObjectName(u"pushButton_edit_keywords")

        self.horizontalLayout_3.addWidget(self.pushButton_edit_keywords)

        self.pushButton_execute = QPushButton(Form)
        self.pushButton_execute.setObjectName(u"pushButton_execute")
        self.pushButton_execute.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.pushButton_execute)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_info = QLabel(Form)
        self.label_info.setObjectName(u"label_info")

        self.verticalLayout_2.addWidget(self.label_info)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"HIGHTLIGHT KEYWORDS", None))
        self.pushButton_select_file.setText(QCoreApplication.translate("Form", u"Select Files (F)", None))
#if QT_CONFIG(shortcut)
        self.pushButton_select_file.setShortcut(QCoreApplication.translate("Form", u"F", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_select_folder.setText(QCoreApplication.translate("Form", u"Select Folder (Shift + F)", None))
#if QT_CONFIG(shortcut)
        self.pushButton_select_folder.setShortcut(QCoreApplication.translate("Form", u"Shift+F", None))
#endif // QT_CONFIG(shortcut)
        self.label_selected_path.setText(QCoreApplication.translate("Form", u"Selected Paths:", None))
        self.label_strategy.setText(QCoreApplication.translate("Form", u"Highlight Strategy:", None))
        self.comboBox_strategy.setItemText(0, QCoreApplication.translate("Form", u"1. Markdown", None))
        self.comboBox_strategy.setItemText(1, QCoreApplication.translate("Form", u"2. Text", None))
        self.comboBox_strategy.setItemText(2, QCoreApplication.translate("Form", u"3. HTML", None))

        self.pushButton_edit_keywords.setText(QCoreApplication.translate("Form", u"Edit Highlight Keywords (E)", None))
#if QT_CONFIG(shortcut)
        self.pushButton_edit_keywords.setShortcut(QCoreApplication.translate("Form", u"E", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_execute.setText(QCoreApplication.translate("Form", u"Execute (Enter)", None))
#if QT_CONFIG(shortcut)
        self.pushButton_execute.setShortcut(QCoreApplication.translate("Form", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.label_info.setText(QCoreApplication.translate("Form", u"Information:", None))
    # retranslateUi

