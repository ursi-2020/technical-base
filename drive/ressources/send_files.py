from flask_restful import reqparse, Resource
from drive.app_dic import get_path
from drive.intelligence.file_manager import File_manager


parser = reqparse.RequestParser()
parser.add_argument('app', type=str, required=True, help='Name of the app which you send the files')
parser.add_argument('path', type=str, required=True, help='the path of the files you want to send')


class Send(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        file_manager = File_manager(args['app'], args['path'])
        file_manager.write()
        return "successfully sent",  200