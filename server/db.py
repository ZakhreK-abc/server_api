import sqlite3
import datetime as dt

class Db:
    def __init__(self):
        self.con = sqlite3.connect("data_base.db")
        self.cursor = self.con.cursor()

    def add(self, data):  # переименовал date в data для ясности
        # Создаем список значений
        values = []
        
        # Добавляем значения из словаря в правильном порядке
        values.append(data['name'])      # 1
        values.append(data['number'])    # 2
        values.append(data['note'])      # 3
        # Добавляем дату
        current_datetime = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        values.append(current_datetime)  # 4

        values.append(data['type'])      # 5
        values.append(data['status'])    # 6
        
        
        
        # Выполняем запрос
        self.cursor.execute("INSERT INTO tab (name, number, note, datetime, type, status) VALUES (?, ?, ?, ?, ?, ?)", values)
        self.con.commit()
        
        return {"status": "success", "id": self.cursor.lastrowid}