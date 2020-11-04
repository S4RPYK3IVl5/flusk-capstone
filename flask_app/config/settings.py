from configparser import ConfigParser
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

parser = ConfigParser()
parser.read("./config/config.ini")

path_to_data_files = parser.get("app_setting", "SQLALCHEMY_DATABASE_URI")
if not os.path.exists(path_to_data_files):
    os.mkdir(path_to_data_files)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/{path_to_data_files}/database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = parser.get("app_setting", "SQLALCHEMY_TRACK_MODIFICATIONS") == "True"
app.config["SECRET_KEY"] = parser.get("app_setting", "SECRET_KEY")

logger_folder_path = parser.get("app_setting", "PATH_TO_LOG_FILE")
if not os.path.exists(logger_folder_path):
    os.mkdir(logger_folder_path)

PATH_TO_LOG_FILE = logger_folder_path + "/log.log"

db = SQLAlchemy(app)
