import traceback
from functools import wraps
from settings import app
import jwt
from flask import request, jsonify
from jsonschema import ValidationError


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
        return f(*args, **kwargs, login=payload['login'])
    return wrapper


def schema_validator_catcher(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            return res
        except ValidationError as ve:
            return {'res': f"Invalid request! {ve.message}"}, 401
    return wrapper


def unwrap_data_from_animal_request(get_request):

    name = str(get_request['name'])
    center = str(get_request['center'])
    species = str(get_request['species'])
    age = str(get_request['age'])
    price = str(get_request.get('price', None))
    description = str(get_request.get('description', None))

    return name, center, species, age, price, description
