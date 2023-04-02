import sys
import sqlite3
from PySide6 import QtWidgets
from MainWindow import Ui_MainWindow
from database import Database
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, AssetsRepository

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        if index == 0:  # Transactions tab
            transactions = transactions_repo.all()
            # Update the Transactions tab with the loaded data
        elif index == 1:  # Income tab
            income_records = income_repo.all()
            # Update the Income tab with the loaded data
        elif index == 2:  # Expenses tab
            expenses_records = expenses_repo.all()
            # Update the Expenses tab with the loaded data
        elif index == 3:  # Loans tab
            loans_records = loans_repo.all()
            # Update the Loans tab with the loaded data
        elif index == 4:  # Assets tab
            assets_records = assets_repo.all()
            # Update the Assets tab with the loaded data



app = QtWidgets.QApplication(sys.argv)

# Initialize the Singleton database connection
db_path = "FinanceDB/FinanceManagerDB.db"
db = Database.instance(db_path)

# Initialize the repositories
transactions_repo = TransactionsRepository(db)
income_repo = IncomeRepository(db)
expenses_repo = ExpensesRepository(db)
loans_repo = LoansRepository(db)
assets_repo = AssetsRepository(db)

window = MainWindow()
window.show()
app.exec_()

# Don't forget to close the database connection when you're done
db.close()
