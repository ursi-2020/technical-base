from flask_restful import reqparse, Resource
from drive.app_dic import add_app_to_dict


parser = reqparse.RequestParser()
parser.add_argument('app', type=str, required=True, help='Name of your app')
parser.add_argument('path', type=str, required=True, help='the path of the directory where you want to recieve'
                                                          ' your files')
parser.add_argument('route', type=str, required=True, help='the POST request drive will call to notify you that a file'
                                                           'was sent')


class Register(Resource):
    def post(self):
        args = parser.parse_args(strict=True)
        add_app_to_dict(args['app'], args['path'], args['route'])
        #request.remote_user
        return "successfully registered",  200