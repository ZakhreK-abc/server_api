from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api()

video = {
    1: {"name": "Python", "number": 16}, 
    2: {"name": "PHP", "number": 21}
}

class Main(Resource):
    def get(self, video_id):
        if video_id == 0:
            return video
        else:
            return video[video_id]
    
    def delete(self, video_id):
        del video[video_id]
        return video
    
    def post(self, video_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("number", type=int)
        video[video_id] = parser.parse_args()
        return video
    
    def put(self, video_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("number", type=int)
        video[video_id] = parser.parse_args()
        return video


api.add_resource(Main, "/api/video/<int:video_id>")
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")
