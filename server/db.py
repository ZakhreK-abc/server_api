import sqlite3
import datetime as dt

class Db:
    def __init__(self):
        self.con = sqlite3.connect("data_base.db")
        self.cursor = self.con.cursor()

    def get(self, selection, mod):
        if selection == 0:
            self.cursor.execute("SELECT * FROM main WHERE status = ?", (mod,))
            data = self.cursor.fetchall()

            return data
        
        elif selection == 1:
            self.cursor.execute("SELECT * FROM main WHERE type = ?", (mod,))
            data = self.cursor.fetchall()

            return data
        
        elif selection == 2:
            self.cursor.execute("SELECT * FROM main WHERE name = ?", (mod,))
            data = self.cursor.fetchall()

            return data
        
        elif selection == 3:
            self.cursor.execute("SELECT * FROM main")
            data = self.cursor.fetchall()

            return data
        
        else:
            return []
        

    def delete(self, id):
        self.cursor.execute("DELETE FROM main WHERE id = ?", (id,))
        # 1. Сдвигаем все ID, которые были больше удаленного
        self.cursor.execute("UPDATE main SET id = id - 1 WHERE id > ?", (id,))

        # 2. Сбрасываем счетчик автоинкремента (чтобы следующий ID был корректным)
        self.cursor.execute("UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM main) WHERE name = 'main'")

        self.con.commit()
        

    def post(self, data):  # переименовал date в data для ясности
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
        self.cursor.execute("INSERT INTO main (name, number, note, datetime, type, status) VALUES (?, ?, ?, ?, ?, ?)", values)
        self.con.commit()
        
        return {"status": "success", "id": self.cursor.lastrowid}
    

    def put(self, id, data):
        values = []

        values.append(data['name'])
        values.append(data['number'])
        values.append(data['note'])
        current_datetime = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        values.append(current_datetime)

        values.append(data['type'])
        values.append(data['status'])
        values.append(id)

        self.cursor.execute(
            "UPDATE main SET name=?, number=?, note=?, datetime=?, type=?, status=? WHERE id=?", 
            values
        )

        self.con.commit()