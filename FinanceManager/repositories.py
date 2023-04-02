# repositories.py
from database import Database

# Base repository class that provides a template for other repository classes
class BaseRepository:
    def __init__(self, db):
        self.db = db

    def all(self):
        raise NotImplementedError

    def create(self, *args):
        raise NotImplementedError

    def read(self, id):
        raise NotImplementedError

    def update(self, id, *args):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

# Repository class for handling transactions table CRUD operations
class TransactionsRepository(BaseRepository):
    def all(self):
        """Retrieve all rows from the transactions table.
        
        Returns:
            list: A list of tuples representing rows in the transactions table.
        """
        query = "SELECT * FROM transactions"
        cursor = self.db.execute_query(query)
        return cursor.fetchall()

    def create(self, income_id, expense_id, amount, date):
        """Create a new transaction."""
        query = "INSERT INTO transactions (income_id, expense_id, amount, date) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (income_id, expense_id, amount, date))

    def read(self, id):
        """
        Retrieve a specific transaction by its ID.
        
        Args:
            id (int): The ID of the transaction to retrieve.
        
        Returns:
            tuple: A tuple representing the transaction row, or None if the transaction is not found.
        """
        query = "SELECT * FROM transactions WHERE id = ?"
        cursor = self.db.execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, income_id, expense_id, amount, date):
        """Update a transaction."""
        query = "UPDATE transactions SET income_id = ?, expense_id = ?, amount = ?, date = ? WHERE id = ?"
        self.db.execute_query(query, (income_id, expense_id, amount, date, id))

    def delete(self, id):
        """Delete a transaction."""
        query = "DELETE FROM transactions WHERE id = ?"
        self.db.execute_query(query, (id,))


class IncomeRepository(BaseRepository):
    def all(self):
        """Retrieve all rows from the income table."""
        query = "SELECT * FROM income"
        cursor = self.db.execute_query(query)
        return cursor.fetchall()

    def create(self, source, amount, date):
        """Create a new income source."""
        query = "INSERT INTO income (source, amount, date) VALUES (?, ?, ?)"
        self.db.execute_query(query, (source, amount, date))

    def read(self, id):
        """Retrieve a specific income source by its ID."""
        query = "SELECT * FROM income WHERE id = ?"
        cursor = self.db.execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, source, amount, date):
        """Update an income source."""
        query = "UPDATE income SET source = ?, amount = ?, date = ? WHERE id = ?"
        self.db.execute_query(query, (source, amount, date, id))

    def delete(self, id):
        """Delete an income source."""
        query = "DELETE FROM income WHERE id = ?"
        self.db.execute_query(query, (id,))

class ExpensesRepository(BaseRepository):
    def all(self):
        """Retrieve all rows from the expenses table."""
        query = "SELECT * FROM expenses"
        cursor = self.db.execute_query(query)
        return cursor.fetchall()

    def create(self, category, amount, date):
        """Create a new expense category."""
        query = "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)"
        self.db.execute_query(query, (category, amount, date))

    def read(self, id):
        """Retrieve a specific expense category by its ID."""
        query = "SELECT * FROM expenses WHERE id = ?"
        cursor = self.db.execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, category, amount, date):
        """Update an expense category."""
        query = "UPDATE expenses SET category = ?, amount = ?, date = ? WHERE id = ?"
        self.db.execute_query(query, (category, amount, date, id))

    def delete(self, id):
        """Delete an expense category."""
        query = "DELETE FROM expenses WHERE id = ?"
        self.db.execute_query(query, (id,))

class LoansRepository(BaseRepository):
    def all(self):
        """Retrieve all rows from the loans table."""
        query = "SELECT * FROM loans"
        cursor = self.db.execute_query(query)
        return cursor.fetchall()

    def create(self, name, amount, interest_rate, start_date):
        """Create a new loan."""
        query = "INSERT INTO loans (name, amount, interest_rate, start_date) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (name, amount, interest_rate, start_date))

    def read(self, id):
        """Retrieve a specific loan by its ID."""
        query = "SELECT * FROM loans WHERE id = ?"
        cursor = self.db.execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, name, amount, interest_rate, start_date):
        """Update a loan."""
        query = "UPDATE loans SET name = ?, amount = ?, interest_rate = ?, start_date = ? WHERE id = ?"
        self.db.execute_query(query, (name, amount, interest_rate, start_date, id))

    def delete(self, id):
        """Delete a loan."""
        query = "DELETE FROM loans WHERE id = ?"
        self.db.execute_query(query, (id,))

class AssetsRepository(BaseRepository):
    def all(self):
        """Retrieve all rows from the assets table."""
        query = "SELECT * FROM assets"
        cursor = self.db.execute_query(query)
        return cursor.fetchall()

    def create(self, name, value, acquisition_date):
        """Create a new asset."""
        query = "INSERT INTO assets (name, value, acquisition_date) VALUES (?, ?, ?)"
        self.db.execute_query(query, (name, value, acquisition_date))

    def read(self, id):
        """Retrieve a specific asset by its ID."""
        query = "SELECT * FROM assets WHERE id = ?"
        cursor = self.db.execute_query(query, (id,))
        return cursor.fetchone()

    def update(self, id, name, value, acquisition_date):
        """Update an asset."""
        query = "UPDATE assets SET name = ?, value = ?, acquisition_date = ? WHERE id = ?"
        self.db.execute_query(query, (name, value, acquisition_date, id))

    def delete(self, id):
        """Delete an asset."""
        query = "DELETE FROM assets WHERE id = ?"
        self.db.execute_query(query, (id,))