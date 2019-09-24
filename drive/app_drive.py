from flask import Flask
from flask_restful import Resource, Api
from drive.ressources.register import Register
from drive.ressources.send_files import Send

app = Flask(__name__)
api = Api(app)

api.add_resource(Register)
api.add_resource(Send)


if __name__ == '__main__':
    app.run(debug=True)