from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem
from MainWindow import Ui_MainWindow
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, AssetsRepository, CategoriesRepository

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, db):
        super().__init__()
        self.setupUi(self)

        self.db = db

        # Initialize the repositories
        self.transactions_repo = TransactionsRepository(db)
        self.income_repo = IncomeRepository(db)
        self.expenses_repo = ExpensesRepository(db)
        self.loans_repo = LoansRepository(db)
        self.assets_repo = AssetsRepository(db)
        self.categories_repo = CategoriesRepository(db)

        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        if index == 0:  # Transactions tab
            #TODO update Dashboard
            pass
        elif index == 1:  # Income tab
            #TODO update Budget
            pass
        elif index == 2:  # Expenses tab
            pass
            # Update the Expenses tab with the loaded data
        elif index == 3:  # Loans tab
            pass
            # Update the Income tab with the loaded data
        elif index == 4:  # Assets tab
            pass
            # Update the Loans tab with the loaded data
        elif index == 5: 
            pass
            # Update the Assets tab with the loaded data
        elif index == 6:
            self.load_transactions()  # Call the load_transactions method
            # Update the Transactions tab with the loaded data

    def load_transactions(self):  # New method to load transactions
        transactions = self.transactions_repo.all()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Account ID', 'Date', 'Amount', 'Category'])

        for transaction in transactions:
            row = [
                QStandardItem(str(transaction[0])),
                QStandardItem(str(transaction[1])),
                QStandardItem(str(transaction[2])),
                QStandardItem(str(transaction[3])),
                QStandardItem(str(transaction[4])),
            ]
            model.appendRow(row)

        self.transactionsTableView.setModel(model)  # Set the model for transactionsTableView

    def closeEvent(self, event):
        self.db.close()