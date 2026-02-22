from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from db import Db

app = Flask(__name__)
api = Api()



class Main(Resource):
    def __init__(self):
        self.db = Db()
    
    def get(self, mod):
        url = request.path
        format_url = url.rsplit('/', 1)[0]

        if format_url == "/api/db/status":
            selection = 0
            data = self.db.get(selection, mod)

            return data
        
        elif format_url == "/api/db/type":
            selection = 1
            data = self.db.get(selection, mod)

            return data
        
        elif format_url == "/api/db/name":
            selection = 2
            data = self.db.get(selection, mod)

            return data
        
        elif format_url == "/api/db":
            selection = 3
            data = self.db.get(selection, mod)

            return data
        
    
    def delete(self, mod):
        self.db.delete(mod)
        return 0
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("number", type=int)
        parser.add_argument("note", type=str)
        parser.add_argument("type", type=str)
        parser.add_argument("status", type=int)
        self.db.post(parser.parse_args())
        return 0
    
    def put(self, mod):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("number", type=int)
        parser.add_argument("note", type=str)
        parser.add_argument("type", type=str)
        parser.add_argument("status", type=int)
        self.db.put(mod, parser.parse_args())
        return 0


api.add_resource(Main,
    "/api/db",
    "/api/db/",
    "/api/db/<int:mod>",
    "/api/db/status/<int:mod>",
    "/api/db/type/<string:mod>",
    "/api/db/name/<string:mod>",
    "/api/db/id/<int:mod>"
)

api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="192.168.111.101")
