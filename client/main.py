import requests
import json
import os
import time

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def show():
    print("===Search-type-of-elements===")
    print("1.Name")
    print("2.Type")
    print("3.Status")
    print("4.back")
    print("===================")
    search = int(input("#"))

    if search == 1:
        print("===Enter-name===")
        name = input("#")

        res = requests.get(f"http://127.0.0.1:5000/api/db/name/{name}")
        print(res.json())

        input("Press enter to continue...")
        clear_terminal()

    if search == 2:
        print("===Enter-type===")
        type = input("#")

        res = requests.get(f"http://127.0.0.1:5000/api/db/type/{type}")
        print(res.json())

        input("Press enter to continue...")
        clear_terminal()

    if search == 3:
        print("===Enter-status===")
        status = int(input("#"))

        res = requests.get(f"http://127.0.0.1:5000/api/db/status/{status}")
        print(res.json())

        input("Press enter to continue...")
        clear_terminal()

    if search == 4:
        clear_terminal()

def add():
    values = {}
    print("===Add-element===")
    print("Yes(y) or No(n)?")
    if input("#") == "y":
        print("===Enter-value===")
        values["name"] = input("#Enter-name: ")
        values["number"] = int(input("#Enter-number: "))
        values["note"] = input("#Enter-note: ")
        values["type"] = input("#Enter-type: ")
        values["status"] = int(input("#Enter-status: "))

        res = requests.post("http://127.0.0.1:5000/api/db", json=values)
        print(res.json())

        time.sleep(3)
        clear_terminal()
    else:
        clear_terminal()

def update():
    print("===Update-element===")
    print("Yes(y) or No(n)?")
    if input("#") == "y":
        print("===Enter-id===")
        id = int(input("#"))

        values = {}
        print("===Enter-value===")
        values["name"] = input("#Enter-name: ")
        values["number"] = int(input("#Enter-number: "))
        values["note"] = input("#Enter-note: ")
        values["type"] = input("#Enter-type: ")
        values["status"] = int(input("#Enter-status: "))

        res = requests.put(f"http://127.0.0.1:5000/api/db/id/{id}", json=values)
        print(res.json())

        time.sleep(3)
        clear_terminal()
    else:
        clear_terminal()

def delete():
    print("===Delete-element===")
    print("Yes(y) or No(n)?")
    if input("#") == "y":
        print("===Enter-id===")
        id = int(input("#"))

        res = requests.delete(f"http://127.0.0.1:5000/api/db/id/{id}")
        print(res.json())

        time.sleep(3)
        clear_terminal()
    else:
        clear_terminal()

print("=====WELCOME-TO-YOUR-DB=====")

while True:
    print("===Search-active===")
    print("1.Show elements")
    print("2.Add element")
    print("3.Update element")
    print("4.Delete element")
    print("5.back")
    print("===================")
    search = int(input("#"))

    if search == 1:
        clear_terminal()
        show()
    elif search == 2:
        clear_terminal()
        add()
    elif search == 3:
        clear_terminal()
        update()
    elif search == 4:
        clear_terminal()
        delete()
    elif search == 5:
        clear_terminal()
        break
    else:
        print("input correct number")
        time.sleep(3)

        clear_terminal()

