import threading
from flask import Flask
from flask_restful import Api
from drive.ressources.register import Register
from drive.ressources.send_files import Send
from drive.ressources.queue_start import Queue
from drive.app_dic import queue_pop
from drive.intelligence.file_manager import write

app = Flask(__name__)
api = Api(app)

api.add_resource(Queue, '/')
api.add_resource(Register, '/register')
api.add_resource(Send, '/send')

if __name__ == '__main__':
    app.run(debug=True)


