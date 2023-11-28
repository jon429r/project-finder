import sqlite3

class Database:
    location = 'database.db'
    def __init__(self) -> None:
        self.connection = sqlite3.connect(self.location)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, directory TEXT')
        self.connection.commit()