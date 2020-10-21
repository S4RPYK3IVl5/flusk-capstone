import traceback
from functools import wraps
from config.settings import app, PATH_TO_LOG_FILE
import jwt
from flask import request, jsonify
from jsonschema import ValidationError
import logging
from flask import request


class NoAccessException(Exception):
    pass


class SpeciesDoesNotExistException(Exception):
    pass


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.get_json().get('token')
        if not token:
            return {"error": "Toke is required"}, 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            traceback.print_exc()
            return jsonify({'error': "Need a valid token to view this page"}), 401
        return f(*args, **kwargs, login=payload['login'], id=payload['id'])
    return wrapper


def requests_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            return res
        except ValidationError as ve:
            send_error_to_log(request.base_url, request.method, ve.message)
            return {'res': f"Invalid request! {ve.message}"}, 401
        except Exception as ex:
            send_error_to_log(request.base_url, request.method, str(ex))
            return {'res': f"Exception had been occurred: {str(ex)}"}
    return wrapper


def unwrap_data_from_animal_request(get_request):

    name = str(get_request['name'])
    center = str(get_request['center'])
    species = str(get_request['species'])
    age = str(get_request['age'])
    price = str(get_request.get('price', None))
    description = str(get_request.get('description', None))

    return name, center, species, age, price, description


formatter = logging.Formatter("%(asctime)s - %(message)s")

handler = logging.FileHandler(PATH_TO_LOG_FILE, mode="a", encoding="UTF-8")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def send_message_to_log(*args):
    logger.info(" - ".join(args))


def send_error_to_log(*args):
    logger.error(" - ".join(args))
