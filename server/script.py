import sqlite3

con =  sqlite3.connect("data_base.db")
cursor = con.cursor()

cursor.execute("""CREATE TABLE main (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               number INTEGER,
               note TEXT,
               datetime TEXT,
               type TEXT,
               status INTEGER
                )""")