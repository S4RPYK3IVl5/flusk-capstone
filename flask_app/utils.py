import traceback
from functools import wraps
from flask_app.config.settings import app, PATH_TO_LOG_FILE
import jwt
from flask import jsonify
from jsonschema import ValidationError
import logging
from flask import request


formatter = logging.Formatter("%(asctime)s - %(message)s")

handler = logging.FileHandler(PATH_TO_LOG_FILE, mode="a", encoding="UTF-8")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class NoAccessException(Exception):
    pass


class SpeciesDoesNotExistException(Exception):
    pass


def token_required(f):
    """
    Wrapper for those request handlers, which needed to be secured by jwt token
    :param f:
        Function, by another word, it is a handler for specific HTTP request
    :return:
        :type object
            A wrapper function
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.form.get('token')
        if not token:
            return {"error": "Token is required"}, 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            traceback.print_exc()
            return jsonify({'error': "Need a valid token to view this page"}), 401
        return f(*args, **kwargs, login=payload['login'], id=payload['id'])
    return wrapper


def requests_handler(f):
    """
    Wrapper for function, which needed to be handled in case of some Error occurrence
    :param f:
        Function, by another word, it is a handler for specific Error
    :return:
        :type object
            A wrapper function
    """
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
            return {'res': f"Exception had been occurred: {str(ex)}"}, 401
    return wrapper


def unwrap_data_from_animal_request(get_request):
    """
    Unwrap animal data from API request
    :param get_request:
        Dictionary of animal data from API request
    :return:
        :type tuple
            A tuple of parameters to create animals
    """
    name = get_request['name']
    center = get_request['center']
    species = get_request['species']
    age = get_request['age']
    price = get_request.get('price', None)
    description = get_request.get('description', None)

    return name, center, species, age, price, description


def send_message_to_log(method, path, center_id, changed_entity, changed_id):
    """
    Log information to file
    :param method:
        Request method parameter. Ex: POST, GET and etc.
    :param path:
        Request URL path.
    :param center_id:
        Center, performed request
    :param changed_entity:
        Changed entity, during the request.
    :param changed_id:
        Id of the changed entity.
    """
    logger.info("%s - %s - %s - %s - %s", method, path, center_id, changed_entity, changed_id)


def send_error_to_log(url, method, message):
    """
    Log errors to file
    :param url:
        Request URL path.
    :param method:
        Request method parameter. Ex: POST, GET and etc.
    :param message:
        Error message.
    """
    logger.error("%s - %s - %s", url, method, message)
