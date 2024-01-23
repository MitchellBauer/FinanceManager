from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QComboBox, QDialog, QMessageBox
from MainWindow import Ui_MainWindow
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, \
    AssetsRepository, CategoriesRepository
from ClassAddIncomeDialog import AddIncomeDialog
from ClassAddExpenseDialog import AddExpenseDialog
from ClassAddLoanDialog import AddLoanDialog


class CategoryDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent, categories):
        super().__init__(parent)
        self.categories = categories

    def createEditor(self, parent, option, index):
        combo_box = QComboBox(parent)
        combo_box.setEditable(True)
        combo_box.addItems(self.categories)
        return combo_box

    def setEditorData(self, editor, index):
        if isinstance(editor, QComboBox):
            value = index.model().data(index, QtCore.Qt.EditRole)
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            model.setData(index, value, QtCore.Qt.EditRole)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, db):
        super().__init__()
        self.setupUi(self)

        self.db = db

        # Initialize the repositories
        self.transactions_repo = TransactionsRepository(db)
        self.income_repo = IncomeRepository(db)
        self.expense_repo = ExpensesRepository(db)
        self.loans_repo = LoansRepository(db)
        self.assets_repo = AssetsRepository(db)
        self.categories_repo = CategoriesRepository(db)

        self.tabWidget.currentChanged.connect(self.on_tab_changed)
        # Set the default tab of the QTabWidget to index 0
        self.tabWidget.setCurrentIndex(0)

        # Transaction Tab
        # Initialize the original transactions data
        self.original_transactions = None

        # Add the save button to the Transactions tab
        self.saveTransactionButton.setEnabled(False)
        self.saveTransactionButton.clicked.connect(self.transaction_save_changes)

        # Income Tab
        # Add the add income button to the Income tab
        self.addIncomeButton.clicked.connect(self.add_income)
        self.deleteIncomeButton.clicked.connect(self.delete_income)
        self.saveIncomeButton.clicked.connect(self.income_update_changes)
        # Initialize the original income data
        self.original_income = None

        # Expenses Tab
        # Add the add expense button to the Expenses tab
        self.addExpenseButton.clicked.connect(self.add_expense)
        self.deleteExpenseButton.clicked.connect(self.delete_expense)
        self.saveExpenseButton.clicked.connect(self.expense_update_changes)
        # Initialize the original expense data
        self.original_expenses = None

        # Loans Tab
        # Add the add loan button to the Loans tab
        self.addLoanButton.clicked.connect(self.add_loan)
        self.deleteLoanButton.clicked.connect(self.delete_loan)
        self.saveLoanButton.clicked.connect(self.loan_update_changes)
        # Initialize the original loan data
        self.original_loans = None

    def on_tab_changed(self, index):
        if index == 0:  # Transactions tab
            # TODO update Dashboard
            pass
        elif index == 1:  # Income tab
            # TODO update Budget
            pass
        elif index == 2:  # Expenses tab
            # Update the Expenses tab with the loaded data
            self.load_expenses()
            self.saveExpenseButton.setEnabled(False)
        elif index == 3:  # Loans tab
            self.load_income()
            self.saveIncomeButton.setEnabled(False)
            # Update the Income tab with the loaded data
        elif index == 4:  # Assets tab
            # Update the Loans tab with the loaded data
            self.load_loans()
            self.saveIncomeButton.setEnabled(False)
        elif index == 5:
            # Update the Assets tab with the loaded data
            pass
        elif index == 6:
            self.load_transactions()  # Call the load_transactions method
            self.saveTransactionButton.setEnabled(False)  # Disable the save button by default

    # Transactions Tab
    def load_transactions(self):  # New method to load transactions
        transactions = self.transactions_repo.all()
        self.original_transactions = transactions.copy()  # Store the original transactions data

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Account ID', 'Date', 'Amount', 'Description', 'Category'])

        categories = self.categories_repo.all()
        category_names = [c[1] for c in categories]
        delegate = CategoryDelegate(self.transactionsTableView, category_names)

        for transaction in transactions:
            row = [
                QStandardItem(str(transaction[0])),
                QStandardItem(str(transaction[1])),
                QStandardItem(str(transaction[2])),
                QStandardItem(str(transaction[3])),
                QStandardItem(str(transaction[4])),
                QStandardItem(str(transaction[5])),
            ]
            for i in range(len(row)):
                if i not in [5]:  # Disable editing for columns ID, Account ID, Date
                    row[i].setEditable(False)
            model.appendRow(row)

        self.transactionsTableView.setModel(model)
        self.transactionsTableView.setItemDelegateForColumn(5, delegate)

        self.transactionsTableView.resizeColumnsToContents()  # Automatically adjust column widths

        # Connect the dataChanged signal of the model to a slot that enables the saveButton
        model.dataChanged.connect(self.transaction_on_data_changed)

    def transaction_on_data_changed(self, topLeft, bottomRight):
        if topLeft.column() == 5:
            self.saveTransactionButton.setEnabled(True)

    def transaction_save_changes(self):
        current_transactions = []
        for row in range(self.transactionsTableView.model().rowCount()):
            transaction = [
                int(self.transactionsTableView.model().index(row, 0).data()),
                int(self.transactionsTableView.model().index(row, 1).data()),
                self.transactionsTableView.model().index(row, 2).data(),
                float(self.transactionsTableView.model().index(row, 3).data()),
                self.transactionsTableView.model().index(row, 4).data(),  # Use index 4 for the Description data
                self.transactionsTableView.model().index(row, 5).data(),  # Use index 5 for the Category data
            ]
            current_transactions.append(transaction)

        # Compare the current transactions data with the original data
        if current_transactions != self.original_transactions:
            # Save the changes to the Transactions table and register new categories and descriptions in the
            # Categories table
            for transaction in current_transactions:
                self.transactions_repo.update_category(transaction[0], transaction[5])

            categories = self.categories_repo.all()
            category_names = [c[1] for c in categories]
            new_categories = set([t[5] for t in current_transactions]).difference(set(category_names))
            descriptions = set([t[4] for t in current_transactions])
            for category, description in zip(new_categories, descriptions):
                self.categories_repo.create(description, category)

            # Reload the transactions data and disable the save button
            self.load_transactions()
            self.saveTransactionButton.setEnabled(False)

        else:
            # Warn the user that there are no changes to save
            QMessageBox.warning(self, "No Changes", "There are no changes to save.")

    def closeEvent(self, event):
        self.db.close()

    # Income Tab, load income data from the database, and update the Income tab, columns ID, Name, Amount, Frequency
    def load_income(self):
        income = self.income_repo.all()
        self.original_income = income.copy()  # Store the original income data

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Name', 'Amount', 'Frequency'])

        for i in income:
            row = [
                QStandardItem(str(i[0])),
                QStandardItem(str(i[1])),
                QStandardItem(str(i[2])),
                QStandardItem(str(i[3])),
            ]
            model.appendRow(row)

        self.incomeTableView.setModel(model)
        self.incomeTableView.resizeColumnsToContents()  # Automatically adjust column widths

        # Connect the dataChanged signal of the model to a slot that enables the saveButton
        model.dataChanged.connect(self.income_on_data_changed)

    def add_income(self):
        dialog = AddIncomeDialog(self, self.income_repo)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.load_income()

    def delete_income(self):
        # Get the selected indexes from the incomeTableView
        selected_indexes = self.incomeTableView.selectedIndexes()

        if selected_indexes:
            # Get the selected row
            row = selected_indexes[0].row()

            # Get the income ID from the first column of the selected row
            income_id = int(self.incomeTableView.model().item(row, 0).text())

            # Delete the income from the SQLite database
            self.income_repo.delete(income_id)

            # Remove the row from the incomeTableView
            self.incomeTableView.model().removeRow(row)

            # Display a message box to inform the user that the row was deleted
            QMessageBox.information(self, "Row Deleted", "The selected row has been deleted.")

        else:
            # Display a message box to inform the user to select a row
            QMessageBox.warning(self, "No Row Selected", "Please select a row to delete.")

    def income_on_data_changed(self, topLeft, bottomRight):
        self.saveIncomeButton.setEnabled(True)

    def income_update_changes(self):
        current_income = []
        for row in range(self.incomeTableView.model().rowCount()):
            income = [
                int(self.incomeTableView.model().index(row, 0).data()),
                self.incomeTableView.model().index(row, 1).data(),
                float(self.incomeTableView.model().index(row, 2).data()),
                self.incomeTableView.model().index(row, 3).data(),
            ]
            current_income.append(income)

        # Compare the current income data with the original data
        if current_income != self.original_income:
            # Save the changes to the Income table
            for income in current_income:
                self.income_repo.update(income[0], income[1], income[2], income[3])

            # Reload the income data and disable the save button
            self.load_income()
            self.saveIncomeButton.setEnabled(False)

        else:
            # Warn the user that there are no changes to save
            QMessageBox.warning(self, "No Changes", "There are no changes to save.")

    # Expenses Tab, load expense data from the database, and update the Expenses tab, columns ID, Name, Amount,
    # Frequency
    def load_expenses(self):
        expenses = self.expense_repo.all()
        self.original_expenses = expenses.copy()  # Store the original expense data

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Name', 'Amount', 'Frequency'])

        for e in expenses:
            row = [
                QStandardItem(str(e[0])),
                QStandardItem(str(e[1])),
                QStandardItem(str(e[2])),
                QStandardItem(str(e[3])),
            ]
            model.appendRow(row)

        self.expenseTableView.setModel(model)
        self.expenseTableView.resizeColumnsToContents()  # Automatically adjust column widths

        # Connect the dataChanged signal of the model to a slot that enables the saveButton
        model.dataChanged.connect(self.expenses_on_data_changed)

    def add_expense(self):
        dialog = AddExpenseDialog(self, self.expense_repo)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.load_expenses()

    def delete_expense(self):
        # Get the selected indexes from the expenseTableView
        selected_indexes = self.expenseTableView.selectedIndexes()

        if selected_indexes:
            # Get the selected row
            row = selected_indexes[0].row()

            # Get the expense ID from the first column of the selected row
            expense_id = int(self.expenseTableView.model().item(row, 0).text())

            # Delete the expense from the SQLite database
            self.expense_repo.delete(expense_id)

            # Remove the row from the expenseTableView
            self.expenseTableView.model().removeRow(row)

            # Display a message box to inform the user that the row was deleted
            QMessageBox.information(self, "Row Deleted", "The selected row has been deleted.")

        else:
            # Display a message box to inform the user to select a row
            QMessageBox.warning(self, "No Row Selected", "Please select a row to delete.")

    def expenses_on_data_changed(self, topLeft, bottomRight):
        self.saveExpenseButton.setEnabled(True)

    def expense_update_changes(self):
        current_expenses = []
        for row in range(self.expenseTableView.model().rowCount()):
            expense = [
                int(self.expenseTableView.model().index(row, 0).data()),
                self.expenseTableView.model().index(row, 1).data(),
                float(self.expenseTableView.model().index(row, 2).data()),
                int(self.expenseTableView.model().index(row, 3).data()),
            ]
            current_expenses.append(expense)

        # Compare the current expense data with the original data
        if current_expenses != self.original_expenses:
            # Save the changes to the Expenses table
            for expense in current_expenses:
                self.expense_repo.update(expense[0], expense[1], expense[2], expense[3])

            # Reload the expense data and disable the save button
            self.load_expenses()
            self.saveExpenseButton.setEnabled(False)

        else:
            # Warn the user that there are no changes to save
            QMessageBox.warning(self, "No Changes", "There are no changes to save.")

    # Loans Tab, load loan data from the database, and update the Loans tab, columns ID, Name, Monthly_Payment,
    # Remaining_Balance, Starting_Date, APR, Last_Payment, Next_Payment
    def load_loans(self):
        loans = self.loans_repo.all()
        self.original_loans = loans.copy()  # Store the original loan data

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Monthly Payment', 'Remaining Balance', 'Starting Date', 'APR', 'Last Payment',
             'Next Payment'])

        for l in loans:
            row = [
                QStandardItem(str(l[0])),
                QStandardItem(str(l[1])),
                QStandardItem(str(l[2])),
                QStandardItem(str(l[3])),
                QStandardItem(str(l[4])),
                QStandardItem(str(l[5])),
                QStandardItem(str(l[6])),
                QStandardItem(str(l[7])),
            ]
            model.appendRow(row)

        self.loanTableView.setModel(model)
        self.loanTableView.resizeColumnsToContents()  # Automatically adjust column widths

        # Connect the dataChanged signal of the model to a slot that enables the saveButton
        model.dataChanged.connect(self.loans_on_data_changed)

    def add_loan(self):
        dialog = AddLoanDialog(self, self.loans_repo)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.load_loans()

    def delete_loan(self):
        # Get the selected indexes from the loanTableView
        selected_indexes = self.loanTableView.selectedIndexes()

        if selected_indexes:
            # Get the selected row
            row = selected_indexes[0].row()

            # Get the loan ID from the first column of the selected row
            loan_id = int(self.loanTableView.model().item(row, 0).text())

            # Delete the loan from the SQLite database
            self.loans_repo.delete(loan_id)

            # Remove the row from the loanTableView
            self.loanTableView.model().removeRow(row)

            # Display a message box to inform the user that the row was deleted
            QMessageBox.information(self, "Row Deleted", "The selected row has been deleted.")

        else:
            # Display a message box to inform the user to select a row
            QMessageBox.warning(self, "No Row Selected", "Please select a row to delete.")

    def loans_on_data_changed(self, topLeft, bottomRight):
        self.saveLoanButton.setEnabled(True)

    def loan_update_changes(self):
        current_loans = []
        for row in range(self.loanTableView.model().rowCount()):
            loan = [
                int(self.loanTableView.model().index(row, 0).data()),
                self.loanTableView.model().index(row, 1).data(),
                float(self.loanTableView.model().index(row, 2).data()),
                float(self.loanTableView.model().index(row, 3).data()),
                self.loanTableView.model().index(row, 4).data(),
                float(self.loanTableView.model().index(row, 5).data()),
                self.loanTableView.model().index(row, 6).data(),
                self.loanTableView.model().index(row, 7).data(),
            ]
            current_loans.append(loan)

        # Compare the current loan data with the original data
        if current_loans != self.original_loans:
            # Save the changes to the Loans table
            for loan in current_loans:
                self.loans_repo.update(loan[0], loan[1], loan[2], loan[3], loan[4], loan[5], loan[6], loan[7])

            # Reload the loan data and disable the save button
            self.load_loans()
            self.saveLoanButton.setEnabled(False)

        else:
            # Warn the user that there are no changes to save
            QMessageBox.warning(self, "No Changes", "There are no changes to save.")


