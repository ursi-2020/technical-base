import threading
from flask_restful import Resource
from app_dic import queue_pop, get_was_get, set_was_get_to_true
from intelligence.file_manager import write


def manage_queue():
    while True:
        (app, path, name_file) = queue_pop()
        if app:
            write(app, path, name_file)


class Queue(Resource):
    @staticmethod
    def get():
        if not get_was_get():
            set_was_get_to_true()
            thread_queue = threading.Thread(target=manage_queue())
            thread_queue.start()
            return 200, "queue started"
        return 200
