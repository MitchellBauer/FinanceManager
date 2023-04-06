import sys
import sqlite3
from PySide6 import QtWidgets, QtSql  # Add QtSql import
from MainWindow import Ui_MainWindow
from database import Database
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, AssetsRepository, CategoriesRepository

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        if index == 0:  # Transactions tab
            #TODO update Dashboard
        elif index == 1:  # Income tab
            #TODO update Budget
        elif index == 2:  # Expenses tab
            expenses_records = expenses_repo.all()
            # Update the Expenses tab with the loaded data
        elif index == 3:  # Loans tab
            income_records = income_repo.all()
            # Update the Income tab with the loaded data
        elif index == 4:  # Assets tab
            loans_records = loans_repo.all()
            # Update the Loans tab with the loaded data
        elif index == 5: 
            assets_records = assets_repo.all()
            # Update the Assets tab with the loaded data
        elif index == 6:
            self.load_transactions()  # Call the load_transactions method
            # Update the Transactions tab with the loaded data

def load_transactions(self):  # New method to load transactions
    transactions = transactions_repo.all()
    model = QtCore.QStandardItemModel()
    model.setHorizontalHeaderLabels(['ID', 'Income ID', 'Expense ID', 'Amount', 'Date'])

    for transaction in transactions:
        row = [
            QtCore.QStandardItem(str(transaction[0])),
            QtCore.QStandardItem(str(transaction[1])),
            QtCore.QStandardItem(str(transaction[2])),
            QtCore.QStandardItem(str(transaction[3])),
            QtCore.QStandardItem(str(transaction[4])),
        ]
        model.appendRow(row)

    self.transactionsTableView.setModel(model)  # Set the model for transactionsTableView

def import_ofx(file_path):
    with open(file_path) as file:
        ofx = OfxParser.parse(file)
    return ofx

def parse_ofx(ofx):
    transactions = []
    for account in ofx.accounts:
        for transaction in account.statement.transactions:
            transactions.append({
                'account_id': account.account_id,  # Add account number/ID
                'date': transaction.date,
                'amount': transaction.amount,
                'description': transaction.memo,
                'category': None,
            })
    return transactions

def insert_update_transactions(transactions_repo, transactions):
    for transaction in transactions:
        existing_transaction = transactions_repo.read_by_description_and_date(transaction['description'], transaction['date'])
        if not existing_transaction:
            transactions_repo.create(transaction['account_id'], transaction['date'], transaction['amount'], transaction['description'], transaction['category'])

def update_categories(categories_repo, transactions_repo):
    transactions = transactions_repo.all()
    for transaction in transactions:
        if transaction['category'] is None:
            category = categories_repo.read_by_description(transaction['description'])
            if category:
                transactions_repo.update(transaction['id'], transaction['account_id'], transaction['date'], transaction['amount'], transaction['description'], category['category'])


def show_warning_dialog():
    warning_dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                           "Warning",
                                           "You need to load an .OFX file.",
                                           QtWidgets.QMessageBox.Ok)
    return warning_dialog.exec_()

def open_file_dialog():
    file_dialog = QtWidgets.QFileDialog()
    file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
    file_dialog.setNameFilters(["OFX files (*.ofx)"])
    if file_dialog.exec_():
        return file_dialog.selectedFiles()[0]
    return None



def main():
    app = QtWidgets.QApplication(sys.argv)

    # Show warning dialog
    show_warning_dialog()

    # Open file explorer dialog
    file_path = open_file_dialog()

    # If a file is selected, load the main application
    if file_path:
            # Initialize the Singleton database connection
        db_path = "FinanceDB/FinanceManagerDB.db"
        db = Database.instance(db_path)

        # Initialize the repositories
        transactions_repo = TransactionsRepository(db)
        income_repo = IncomeRepository(db)
        expenses_repo = ExpensesRepository(db)
        loans_repo = LoansRepository(db)
        assets_repo = AssetsRepository(db)
        categories_repo = CategoriesRepository(db)

        # Import .OFX file
        ofx = import_ofx(file_path)

        # Parse the .OFX file and get transaction data.
        transactions = parse_ofx(ofx)

        # Insert or update transactions.
        insert_update_transactions(transactions_repo, transactions)
        update_categories(categories_repo, transactions_repo)

        window = MainWindow()
        window.show()
        app.exec_()

        # Don't forget to close the database connection when you're done
        db.close()
    else:
        sys.exit()

if __name__ == '__main__':
    main()
