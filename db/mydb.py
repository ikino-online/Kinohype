import sqlite3


class Database:

    def __init__(self, dbpath: str):
        self.connect = sqlite3.connect(dbpath)
        self.cursor = self.connect.cursor()
