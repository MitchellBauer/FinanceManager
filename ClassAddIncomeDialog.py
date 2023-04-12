# add_income_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDoubleSpinBox, QPushButton, QComboBox


class AddIncomeDialog(QDialog):
    def __init__(self, parent=None, income_repo=None):
        super().__init__(parent)

        self.income_repo = income_repo

        layout = QVBoxLayout(self)

        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.amount_label = QLabel("Amount")
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(2147483647)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)

        self.frequency_label = QLabel("Frequency")
        self.frequency_input = QComboBox()
        self.frequency_input.addItems(["Bi-Monthly", "Monthly", "Yearly"])
        layout.addWidget(self.frequency_label)
        layout.addWidget(self.frequency_input)

        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save)

    def convert_frequency(self, frequency_text):
        if frequency_text == "Bi-Monthly":
            return 2
        elif frequency_text == "Monthly":
            return 1
        elif frequency_text == "Yearly":
            return 1 / 12

    def save(self):
        name = self.name_input.text()
        amount = self.amount_input.value()
        frequency_text = self.frequency_input.currentText()
        frequency = self.convert_frequency(frequency_text)

        # Save the data to the SQLite database
        self.income_repo.create(name, amount, frequency)

        # Close the dialog
        self.accept()
