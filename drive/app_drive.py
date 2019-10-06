from drive.ressources.register import Register
from drive.ressources.send_files import Send
from drive.ressources.manage_file import Manage
from drive.db import recreate_database, create_app
from drive.db import app, api

#api.add_resource(Queue, '/')
api.add_resource(Register, '/register')
api.add_resource(Send, '/send')
api.add_resource(Manage, '/manage')

if __name__ == '__main__':
    create_app()
    #recreate_database()
    app.run(debug=True)

