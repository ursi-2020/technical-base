import json
from flask import Response
from flask_restful import reqparse, Resource
from models import App, Send_files
from db import db

parser = reqparse.RequestParser()
parser.add_argument('me', type=str, required=True, help='Name of your app')
parser.add_argument('app', type=str, required=True, help='Name of the app which you send the files')
parser.add_argument('path', type=str, required=True, help='the path of the files you want to send')
parser.add_argument('name_file', type=str, required=False, help='the name of the files -- optional')


class Send(Resource):
    def post(self):
        args = parser.parse_args(strict=True)

        me = App.query.filter_by(name=args['me']).first()
        if me is None:
            return Response(
                response=json.dumps(dict(error='You did not register in our Drive plz use the register endpoint')),
                status=400, mimetype='application/json')

        app = App.query.filter_by(name=args['app']).first()
        if app is None:
            return Response(
                response=json.dumps(dict(error='App doesn\'t exist or did not register in our drive')),
                status=400, mimetype='application/json')

        name_file = args['name_files'] if args['name_files'] is not None else args['me']
        new_file_to_send = Send_files(name_app_sending=args['me'], name_app_receive=args['app'],
                                      path_file=args['path'], name_new_file=name_file)

        db.session.add(new_file_to_send)
        db.session.commit()

        return Response(
            response=json.dumps(dict(info='File successfully append to the sending queue')),
            status=200, mimetype='application/json')
