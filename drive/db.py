from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
db = SQLAlchemy()


def create_app():
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def recreate_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
