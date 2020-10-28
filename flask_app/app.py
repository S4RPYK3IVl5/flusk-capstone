import datetime
import traceback

import jsonschema
import jwt
from flask import request

from flask_app.models.access_request import AccessRequest
from flask_app.models.animals import Animals
from flask_app.models.center import Center
from flask_app.models.species import Species
from flask_app.schemas import request_schemas
from flask_app.config.settings import app
from flask_app.utils import requests_handler, token_required, unwrap_data_from_animal_request, send_message_to_log, \
    NoAccessException, SpeciesDoesNotExistException

APPLICATION_JSON = "application/json"


@app.route("/login", methods=["POST"])
@requests_handler
def login_in():
    """
        This API is used for login processing and returning token to an user
        responses:
          401:
            description: incorrect login or password
          200:
            description: return token to user
        returns:
          type: dict
    """
    get_request = request.form
    jsonschema.validate(get_request, request_schemas.login_center_schema)
    login = get_request['login']
    password = get_request['password']

    if Center.is_center_exist(login, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        id_center = str(Center.get_center_by_login(login).id)
        token = jwt.encode({'exp': expiration_date, 'login': login, 'id': id_center},
                           app.config['SECRET_KEY'], algorithm="HS256")
        AccessRequest.register_access_request(login, datetime.datetime.now())
        send_message_to_log("POST", "/login", id_center, "center", id_center)
        return {'token': token}, 200
    else:
        return {'res': 'Incorrect login or password'}, 401


@app.route('/animals', methods=["GET"])
@requests_handler
def get_all_animals():
    """
        This API is used for retrieving all animals in database
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {'animals': Animals.get_all_animals()}, 200


@app.route('/animals/<int:id>', methods=["GET"])
@requests_handler
def get_certain_animal(id):
    """
        This API is used for retrieving certain animal by its id
        parameters:
          - name: id
            type: string
            required: true
            description: the id of animal
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {'animal': Animals.get_certain_animal(id)}, 200


@app.route('/centers', methods=["GET"])
@requests_handler
def get_all_centers():
    """
        This API is used for retrieving all centers
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {"centers": Center.get_all_centers()}, 200


@app.route('/centers/<int:id>', methods=["GET"])
@requests_handler
def get_certain_center(id):
    """
        This API is used for retrieving certain center by its id
        parameters:
          - name: id
            type: string
            required: true
            description: the id of center
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {"center": Center.get_certain_center(id)}, 200


@app.route('/species', methods=["GET"])
@requests_handler
def get_all_species():
    """
        This API is used for retrieving all species
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {'species': Species.get_all_species()}, 200


@app.route('/species/<int:id>', methods=["GET"])
@requests_handler
def get_concrete_species(id):
    """
        This API is used for retrieving certain specie by its id
        parameters:
          - name: id
            type: string
            required: true
            description: the id of specie
        responses:
          200:
            description: -
        returns:
          type: dict
    """
    return {'specie': Species.get_concrete_species_by_id(id)}, 200


@app.route('/register', methods=["POST"])
@requests_handler
def register_center():
    """
        This API is used for creating center and save its instance to db
        responses:
          200:
            description: Center was successfully registered
        returns:
          type: dict
    """
    get_request = request.form
    jsonschema.validate(get_request, request_schemas.register_center_schema)
    login = get_request['login']
    password = get_request['password']
    address = get_request['address']

    center_id = str(Center.create_center(login, password, address))
    send_message_to_log("POST", "/register", center_id, "center", center_id)

    return {'res': "Center was successfully registered"}, 200


@app.route('/animals', methods=["POST"])
@token_required
@requests_handler
def register_animal(**kwargs):
    """
        This API is used for creating animals and save its instance to db
        responses:
          401:
            description: No such species '{species}' exist, please, create it firstly
          200:
            description: Animal was created
        returns:
          type: dict
    """
    get_request = request.form
    jsonschema.validate(get_request, request_schemas.register_update_animal_schema)
    name, center, species, age, price, description = unwrap_data_from_animal_request(get_request)

    try:
        id_animal = Animals.create_animal(name, center, species, age, price, description)
        send_message_to_log("POST", "/animals", kwargs['id'], "animal", str(id_animal))
        return {'res': "Animal was created"}, 200
    except SpeciesDoesNotExistException:
        traceback.print_exc()
        return {'res': f"No such species '{species}' exist, please, create it firstly"}, 401


@app.route('/species', methods=["POST"])
@token_required
@requests_handler
def register_species(**kwargs):
    """
        This API is used for creating specie and save its instance to db
        responses:
          200:
            description: Species was successfully registered
        returns:
          type: dict
    """
    get_request = request.form
    jsonschema.validate(get_request, request_schemas.register_species_schema)
    name = get_request['name']
    description = get_request['description']
    price = get_request['price']

    id_species = Species.create_species(name, description, price)
    send_message_to_log("POST", "/species", kwargs['id'], "species", str(id_species))

    return {'res': "Species was successfully registered"}, 200


@app.route('/animals/<int:animal_id>', methods=["PUT"])
@token_required
@requests_handler
def replace_animal(animal_id, **kwargs):
    """
        This API is used for substitute all data for certain animal
        parameters:
          - name: animal_id
            type: string
            required: true
            description: the id of animal
        responses:
          200:
            description: Animal was successfully updated
        returns:
          type: dict
    """
    get_request = request.form
    jsonschema.validate(get_request, request_schemas.register_update_animal_schema)
    name, center, species, age, price, description = unwrap_data_from_animal_request(get_request)

    Animals.update_animal(animal_id, name, center, species, description, age, price)
    send_message_to_log("PUT", f"/animals/{animal_id}", kwargs['id'], "animal", str(animal_id))

    return {'res': "Animal was successfully updated"}, 200


@app.route('/animals/<int:animal_id>', methods=["DELETE"])
@token_required
@requests_handler
def delete_animal(animal_id, **kwargs):
    """
        This API is used for delete certain animal from db
        parameters:
          - name: animal_id
            type: string
            required: true
            description: the id of animal
        responses:
          200:
            description: Animal was deleted
          401:
            description: This center is not owner of this animal
        returns:
          type: dict
    """
    try:
        Animals.delete_animal(animal_id, kwargs['login'])
        send_message_to_log("DELETE", f"/animals/{animal_id}", kwargs['id'], "animal", str(animal_id))
        return {'res': "Animal was deleted"}, 200
    except NoAccessException:
        traceback.print_exc()
        return {'res': "This center is not owner of this animal"}, 401


if __name__ == '__main__':
    app.run(port="8081")
