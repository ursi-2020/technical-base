from flask_restful import reqparse, Resource
import json
from flask import Response
from intelligence.file_manager import write
from models import Send_files, App
from db import db


#parser = reqparse.RequestParser()
#parser.add_argument('nb_files', type=int, required=True, help='Number of files to send')


class Manage(Resource):
    def post(self):
        #args = parser.parse_args(strict=True)
        #nb = args['nb_files']
        b = True

        for i in range(0, 1000):
            sender = Send_files.query.first()
            if sender is None:
                continue
            reciever = App.query.filter_by(name=sender.name_app_receive).first()
            b = b and write(sender.name_app_sending, sender.path_file, sender.name_new_file, reciever)
            dele = Send_files.query.first()
            db.session.delete(dele)
            db.session.commit()
        if b:
            return Response(
                response=json.dumps(dict(info='each iteration made')),
                status=200, mimetype='application/json')
        return Response(
            response=json.dumps(dict(info='we got some errors in sending files')),
            status=404, mimetype='application/json')
