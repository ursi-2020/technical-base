import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://drive:6KXdrj99Q@127.0.0.1:5432/drive'
    #SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://postgres:290442@localhost:5432/ursi_test'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
