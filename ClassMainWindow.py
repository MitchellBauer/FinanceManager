from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QComboBox, QDialog
from MainWindow import Ui_MainWindow
from repositories import TransactionsRepository, IncomeRepository, ExpensesRepository, LoansRepository, \
    AssetsRepository, CategoriesRepository
from ClassAddIncomeDialog import AddIncomeDialog


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
        self.expenses_repo = ExpensesRepository(db)
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

    def on_tab_changed(self, index):
        if index == 0:  # Transactions tab
            # TODO update Dashboard
            pass
        elif index == 1:  # Income tab
            # TODO update Budget
            pass
        elif index == 2:  # Expenses tab
            pass
            # Update the Expenses tab with the loaded data
        elif index == 3:  # Loans tab
            self.load_income()
            self.saveIncomeButton.setEnabled(False)
            # Update the Income tab with the loaded data
        elif index == 4:  # Assets tab
            pass
            # Update the Loans tab with the loaded data
        elif index == 5:
            pass
            # Update the Assets tab with the loaded data
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
            QtWidgets.QMessageBox.warning(self, "No Changes", "There are no changes to save.")

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
            QtWidgets.QMessageBox.information(self, "Row Deleted", "The selected row has been deleted.")

        else:
            # Display a message box to inform the user to select a row
            QtWidgets.QMessageBox.warning(self, "No Row Selected", "Please select a row to delete.")

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
            QtWidgets.QMessageBox.warning(self, "No Changes", "There are no changes to save.")
