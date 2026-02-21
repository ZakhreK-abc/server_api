import requests
import json


res = requests.post("http://127.0.0.1:5000/api/db", json={"name": "Golang", "number": 83, "note": "testing add function", "type": "actions", "status": 1})


# print(res.json())
