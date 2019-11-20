from flask_restful import reqparse, Resource
import json
from flask import Response
from models import App
from db import db

parser = reqparse.RequestParser()
parser.add_argument('app', type=str, required=True, help='Name of your app')
parser.add_argument('path', type=str, required=True, help='the path of the directory where you want to recieve'
                                                          ' your files')
parser.add_argument('route', type=str, required=True, help='the POST request drive will call to notify you that a file'
                                                           'was sent')


class Register(Resource):
    @staticmethod
    def post():
        args = parser.parse_args(strict=True)

        app = App.query.filter_by(name=args['app']).first()
        if app is not None:
            return Response(
                response=json.dumps(dict(error='App exist, you are already registered with this name')),
                status=400, mimetype='application/json')

        try:
            new_app = App(name=args['app'], path_folder=args['path'], route=args['route'])

        except Exception as e:
            print(e)

        db.session.add(new_app)
        db.session.commit()

        return Response(
            response=json.dumps(dict(info='you are successfully registered')),
            status=200, mimetype='application/json')
