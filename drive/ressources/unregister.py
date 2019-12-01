from flask_restful import reqparse, Resource
import json
from flask import Response
from models import App, Send_files
from db import db

parser = reqparse.RequestParser()
parser.add_argument('app', type=str, required=True, help='Name of your app')


class Unregister(Resource):
    @staticmethod
    def post():
        args = parser.parse_args(strict=True)

        try:
            app = App.query.filter_by(name=args['app']).first()
        except Exception as e:
            print(e)
        if app is None:
            return Response(
                response=json.dumps(dict(error='App does not exist')),
                status=400, mimetype='application/json')

        send = Send_files.query.filter_by(name_app_sending=args['app']).first()

        if send is None:
            return Response(
                response=json.dumps(dict(info='App never sent something')),
                status=200, mimetype='application/json')

        db.session.delete(send)
        db.session.commit()

        db.session.delete(app)
        db.session.commit()


        return Response(
            response=json.dumps(dict(info='you are successfully unregister')),
            status=200, mimetype='application/json')
