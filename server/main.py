from flask import Flask
from flask_restful import Api, Resource, reqparse
from db import Db

app = Flask(__name__)
api = Api()



class Main(Resource):
    def __init__(self):
        self.db = Db()
    
    # def get(self, video_id):
    #     pass
    
    # def delete(self, video_id):
    #     del video[video_id]
    #     return video
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("number", type=int)
        parser.add_argument("note", type=str)
        parser.add_argument("type", type=str)
        parser.add_argument("status", type=int)
        self.db.add(parser.parse_args())
        return 0
    
    # def put(self, video_id):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument("name", type=str)
    #     parser.add_argument("number", type=int)
    #     video[video_id] = parser.parse_args()
    #     return video


api.add_resource(Main, "/api/db", "/api/db/")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
