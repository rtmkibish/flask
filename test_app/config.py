import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))

with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = config.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    MAIL_SERVER = config.get("MAIL_SERVER")
    MAIL_PORT = config.get("MAIL_PORT")
    MAIL_USE_TLS = config.get("MAIL_USE_TLS")
    MAIL_USE_SSL = config.get("MAIL_USE_SSL")
    MAIL_USERNAME = config.get("MAIL_USERNAME")
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")