from configparser import ConfigParser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

parser = ConfigParser()
parser.read("./config/config.ini")

app.config["SQLALCHEMY_DATABASE_URI"] = parser.get("app_setting", "SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = parser.get("app_setting", "SQLALCHEMY_TRACK_MODIFICATIONS") == "True"
app.config["SECRET_KEY"] = parser.get("app_setting", "SECRET_KEY")

PATH_TO_LOG_FILE = parser.get("app_setting", "PATH_TO_LOG_FILE")

db = SQLAlchemy(app)
