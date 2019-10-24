from ressources.register import Register
from ressources.send_files import Send
from ressources.manage_file import Manage
from db import recreate_database, create_app
from db import app, api

#api.add_resource(Queue, '/')
api.add_resource(Register, '/register')
api.add_resource(Send, '/send')
api.add_resource(Manage, '/manage')

if __name__ == '__main__':
    create_app()
    #recreate_database()
    app.run(host='0.0.0.0', port=5001)

