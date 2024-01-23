# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(803, 590)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 801, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.dashboardTab = QWidget()
        self.dashboardTab.setObjectName(u"dashboardTab")
        self.tabWidget.addTab(self.dashboardTab, "")
        self.budgetTab = QWidget()
        self.budgetTab.setObjectName(u"budgetTab")
        self.tabWidget.addTab(self.budgetTab, "")
        self.expensesTab = QWidget()
        self.expensesTab.setObjectName(u"expensesTab")
        self.expenseTableView = QTableView(self.expensesTab)
        self.expenseTableView.setObjectName(u"expenseTableView")
        self.expenseTableView.setGeometry(QRect(0, 0, 801, 431))
        self.addExpenseButton = QPushButton(self.expensesTab)
        self.addExpenseButton.setObjectName(u"addExpenseButton")
        self.addExpenseButton.setGeometry(QRect(10, 460, 93, 28))
        self.deleteExpenseButton = QPushButton(self.expensesTab)
        self.deleteExpenseButton.setObjectName(u"deleteExpenseButton")
        self.deleteExpenseButton.setGeometry(QRect(120, 460, 93, 28))
        self.saveExpenseButton = QPushButton(self.expensesTab)
        self.saveExpenseButton.setObjectName(u"saveExpenseButton")
        self.saveExpenseButton.setGeometry(QRect(240, 460, 93, 28))
        self.tabWidget.addTab(self.expensesTab, "")
        self.incomeTab = QWidget()
        self.incomeTab.setObjectName(u"incomeTab")
        self.incomeTableView = QTableView(self.incomeTab)
        self.incomeTableView.setObjectName(u"incomeTableView")
        self.incomeTableView.setGeometry(QRect(0, 0, 801, 411))
        self.addIncomeButton = QPushButton(self.incomeTab)
        self.addIncomeButton.setObjectName(u"addIncomeButton")
        self.addIncomeButton.setGeometry(QRect(30, 450, 93, 28))
        self.saveIncomeButton = QPushButton(self.incomeTab)
        self.saveIncomeButton.setObjectName(u"saveIncomeButton")
        self.saveIncomeButton.setGeometry(QRect(230, 450, 93, 28))
        self.deleteIncomeButton = QPushButton(self.incomeTab)
        self.deleteIncomeButton.setObjectName(u"deleteIncomeButton")
        self.deleteIncomeButton.setGeometry(QRect(130, 450, 93, 28))
        self.tabWidget.addTab(self.incomeTab, "")
        self.loansTab = QWidget()
        self.loansTab.setObjectName(u"loansTab")
        self.loanTableView = QTableView(self.loansTab)
        self.loanTableView.setObjectName(u"loanTableView")
        self.loanTableView.setGeometry(QRect(0, 0, 801, 431))
        self.addLoanButton = QPushButton(self.loansTab)
        self.addLoanButton.setObjectName(u"addLoanButton")
        self.addLoanButton.setGeometry(QRect(20, 460, 93, 28))
        self.deleteLoanButton = QPushButton(self.loansTab)
        self.deleteLoanButton.setObjectName(u"deleteLoanButton")
        self.deleteLoanButton.setGeometry(QRect(140, 460, 93, 28))
        self.saveLoanButton = QPushButton(self.loansTab)
        self.saveLoanButton.setObjectName(u"saveLoanButton")
        self.saveLoanButton.setGeometry(QRect(250, 460, 93, 28))
        self.tabWidget.addTab(self.loansTab, "")
        self.assetsTab = QWidget()
        self.assetsTab.setObjectName(u"assetsTab")
        self.tabWidget.addTab(self.assetsTab, "")
        self.transactionsTab = QWidget()
        self.transactionsTab.setObjectName(u"transactionsTab")
        self.transactionsTableView = QTableView(self.transactionsTab)
        self.transactionsTableView.setObjectName(u"transactionsTableView")
        self.transactionsTableView.setGeometry(QRect(0, 0, 791, 441))
        self.transactionsTableView.setAutoFillBackground(False)
        self.saveTransactionButton = QPushButton(self.transactionsTab)
        self.saveTransactionButton.setObjectName(u"saveTransactionButton")
        self.saveTransactionButton.setEnabled(False)
        self.saveTransactionButton.setGeometry(QRect(660, 470, 93, 28))
        self.tabWidget.addTab(self.transactionsTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 803, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dashboardTab), QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.budgetTab), QCoreApplication.translate("MainWindow", u"Budget", None))
        self.addExpenseButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteExpenseButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.saveExpenseButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.expensesTab), QCoreApplication.translate("MainWindow", u"Expenses", None))
        self.addIncomeButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.saveIncomeButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.deleteIncomeButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.incomeTab), QCoreApplication.translate("MainWindow", u"Income", None))
        self.addLoanButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteLoanButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.saveLoanButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.loansTab), QCoreApplication.translate("MainWindow", u"Loans", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.assetsTab), QCoreApplication.translate("MainWindow", u"Assets", None))
        self.saveTransactionButton.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.transactionsTab), QCoreApplication.translate("MainWindow", u"Transactions", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

