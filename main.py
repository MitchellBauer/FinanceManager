import sys
import sqlite3
from PySide6 import QtWidgets
from database import Database
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, \
    AssetsRepository, CategoriesRepository
from ofxparse import OfxParser
from ClassMainWindow import MainWindow


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
        existing_transaction = transactions_repo.read_by_description_and_date(transaction['description'],
                                                                              transaction['date'])
        if not existing_transaction:
            transactions_repo.create(transaction['account_id'], transaction['date'], transaction['amount'],
                                     transaction['description'], transaction['category'])


def update_categories(categories_repo, transactions_repo):
    transactions = transactions_repo.all()
    for transaction in transactions:
        if transaction['category'] is None:
            category = categories_repo.read_by_description(transaction['description'])
            if category:
                transactions_repo.update(transaction['id'], transaction['account_id'], transaction['date'],
                                         transaction['amount'], transaction['description'], category['category'])


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

    skip_dialog = True

    if not skip_dialog:
        # Show warning dialog
        show_warning_dialog()

        # Open file explorer dialog
        file_path = open_file_dialog()

        # If a file is selected, load the main application
        if file_path:
            # Initialize the Singleton database connection
            db_path = "FinanceDB/FinanceManagerDB.db"
            db = Database.instance(db_path)

            # Import .OFX file
            ofx = import_ofx(file_path)

            # Parse the .OFX file and get transaction data.
            transactions = parse_ofx(ofx)

            # Insert or update transactions.
            insert_update_transactions(TransactionsRepository(db), transactions)
            update_categories(CategoriesRepository(db), TransactionsRepository(db))

            window = MainWindow(db)
            window.show()
            app.exec_()

            # Don't forget to close the database connection when you're done
            db.close()
        else:
            sys.exit()
    else:
        # Initialize the Singleton database connection
        db_path = "FinanceDB/FinanceManagerDB.db"
        db = Database.instance(db_path)

        window = MainWindow(db)
        window.show()
        app.exec()

        # Don't forget to close the database connection when you're done
        db.close()


if __name__ == '__main__':
    main()
