from sqlalchemy.ext.declarative import declarative_base
from db import db
from to_json import OutputMixin

Base = declarative_base()


class App(OutputMixin, db.Model):
    __tablename__ = 'App'
    name = db.Column(db.String, primary_key=True, nullable=False)
    path_folder = db.Column(db.String, nullable=False)
    route = db.Column(db.String, nullable=False)

class Send_files(OutputMixin, db.Model):
    __tablename__ = 'Send_files'
    id = db.Column(db.Integer, primary_key=True)
    name_app_sending = db.Column(db.Integer, nullable=False)
    name_app_receive = db.Column(db.Integer, nullable=False)
    path_file = db.Column(db.String, nullable=False)
    name_new_file = db.Column(db.String, nullable=False)