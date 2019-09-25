from flask_restful import reqparse, Resource
from drive.app_dic import append_queue


parser = reqparse.RequestParser()
parser.add_argument('app', type=str, required=True, help='Name of the app which you send the files')
parser.add_argument('path', type=str, required=True, help='the path of the files you want to send')
parser.add_argument('name_file', type=str, required=False, help='the name of the files -- optional')

class Send(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        file_name = args['name_file']
        if (not file_name):
            file_name = args['app']
        append_queue(args['app'], args['path'], file_name)
        return "successfully sent",  200