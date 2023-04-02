# database.py
import sqlite3

class Database:
    _instance = None

    @classmethod
    def instance(cls, db_path):
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance

    def __init__(self, db_path):
        if self._instance is not None:
            raise Exception("This class is a singleton!")
        self.db_connection = sqlite3.connect(db_path)
        self._instance = self

    def execute_query(self, query, parameters=()):
        with self.db_connection:
            cursor = self.db_connection.cursor()
            cursor.execute(query, parameters)
            return cursor

    def close(self):
        self.db_connection.close()
