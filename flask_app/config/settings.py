from configparser import ConfigParser
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

path_to_app = os.getcwd()
APP_SETTING = "app_setting"

parser = ConfigParser()
parser.read(f"{path_to_app}/config/config.ini")

path_to_data_files = parser.get(APP_SETTING, "SQLALCHEMY_DATABASE_URI")
if not os.path.exists(path_to_data_files):
    os.mkdir(path_to_data_files)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path_to_app}/{path_to_data_files}/database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = parser.get(APP_SETTING, "SQLALCHEMY_TRACK_MODIFICATIONS") == "True"
app.config["SECRET_KEY"] = parser.get(APP_SETTING, "SECRET_KEY")

logger_folder_path = f"{path_to_app}/{parser.get(APP_SETTING, 'PATH_TO_LOG_FILE')}"
if not os.path.exists(logger_folder_path):
    os.mkdir(logger_folder_path)

PATH_TO_LOG_FILE = logger_folder_path + "/log.log"

db = SQLAlchemy(app)
