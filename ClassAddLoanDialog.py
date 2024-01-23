from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox,
                               QPushButton, QDateEdit)


class AddLoanDialog(QDialog):
    def __init__(self, parent=None, loan_repo=None):
        super().__init__(parent)

        self.loan_repo = loan_repo

        layout = QVBoxLayout(self)

        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.monthly_payment_label = QLabel("Monthly Payment")
        self.monthly_payment_input = QDoubleSpinBox()
        self.monthly_payment_input.setMaximum(2147483647)
        layout.addWidget(self.monthly_payment_label)
        layout.addWidget(self.monthly_payment_input)

        self.remaining_balance_label = QLabel("Remaining Balance")
        self.remaining_balance_input = QDoubleSpinBox()
        self.remaining_balance_input.setMaximum(2147483647)
        layout.addWidget(self.remaining_balance_label)
        layout.addWidget(self.remaining_balance_input)

        self.starting_date_label = QLabel("Starting Date")
        self.starting_date_input = QDateEdit()
        self.starting_date_input.setDate(QDate.currentDate())
        layout.addWidget(self.starting_date_label)
        layout.addWidget(self.starting_date_input)

        self.apr_label = QLabel("APR")
        self.apr_input = QDoubleSpinBox()
        self.apr_input.setMaximum(100)
        self.apr_input.setDecimals(2)
        layout.addWidget(self.apr_label)
        layout.addWidget(self.apr_input)

        self.last_payment_label = QLabel("Last Payment")
        self.last_payment_input = QDateEdit()
        self.last_payment_input.setDate(QDate.currentDate())
        layout.addWidget(self.last_payment_label)
        layout.addWidget(self.last_payment_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save)

    def save(self):
        name = self.name_input.text()
        monthly_payment = self.monthly_payment_input.value()
        remaining_balance = self.remaining_balance_input.value()
        starting_date = self.starting_date_input.date().toString("yyyy-MM-dd")
        apr = self.apr_input.value()
        last_payment = self.last_payment_input.date().toString("yyyy-MM-dd")

        # Calculate next_payment by adding 30 days to the last_payment
        next_payment = self.last_payment_input.date().addDays(30).toString("yyyy-MM-dd")

        # Save the data to the SQLite database
        self.loan_repo.create(name, monthly_payment, remaining_balance, starting_date, apr, last_payment, next_payment)

        # Close the dialog
        self.accept()