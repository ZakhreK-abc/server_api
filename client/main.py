import requests
import json

res = requests.put("http://127.0.0.1:5000/api/video/2", json={"name": "C", "number": 36})

print(res.json())
