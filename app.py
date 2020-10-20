import datetime
import traceback

import jsonschema
import jwt
from flask import request

from models.access_request import AccessRequest
from models.animals import Animals
from models.center import Center
from models.species import Species
from schemas import request_schemas
from config.settings import app
from utils import schema_validator_catcher, token_required, unwrap_data_from_animal_request, seng_message_to_log

APPLICATION_JSON = "application/json"


@app.route("/login", methods=["POST"])
@schema_validator_catcher
def login_in():
    get_request = request.get_json()
    jsonschema.validate(get_request, request_schemas.login_center_schema)
    login = str(get_request['login'])
    password = str(get_request['password'])

    if Center.is_center_exist(login, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        id_center = str(Center.get_center_by_login(login).id)
        token = jwt.encode({'exp': expiration_date, 'login': login, 'id': id_center},
                           app.config['SECRET_KEY'], algorithm="HS256")
        AccessRequest.register_access_request(login, datetime.datetime.now())
        seng_message_to_log("POST", "/login", id_center, "center", id_center)
        return {'token': token}
    else:
        return {'res': 'Incorrect login or password'}, 401


@app.route('/animals', methods=["GET"])
def get_all_animals():
    return {'animals': Animals.get_all_animals()}, 200


@app.route('/animals/<int:id>', methods=["GET"])
def get_certain_animal(id):
    return {'animal': Animals.get_certain_animal(id)}, 200


@app.route('/centers', methods=["GET"])
def get_all_centers():
    return {"centers": Center.get_all_centers()}, 200


@app.route('/centers/<int:id>', methods=["GET"])
def get_certain_center(id):
    return {"center": Center.get_certain_center(id)}, 200


@app.route('/species', methods=["GET"])
def get_all_species():
    return {'species': Species.get_all_species()}, 200


@app.route('/species/<int:id>', methods=["GET"])
def get_concrete_species(id):
    return {'specie': Species.get_concrete_species_by_id(id)}, 200


@app.route('/register', methods=["POST"])
@schema_validator_catcher
def register_center():

    get_request = request.get_json()
    jsonschema.validate(get_request, request_schemas.register_center_schema)
    login = str(get_request['login'])
    password = str(get_request['password'])
    address = str(get_request['address'])

    center_id = str(Center.create_center(login, password, address))
    seng_message_to_log("POST", "/register", center_id, "center", center_id)

    return {'res': "Center was successfully registered"}, 200


@app.route('/animals', methods=["POST"])
@token_required
@schema_validator_catcher
def register_animal(**kwargs):

    get_request = request.get_json()
    jsonschema.validate(get_request, request_schemas.register_update_animal_schema)
    name, center, species, age, price, description = unwrap_data_from_animal_request(get_request)

    try:
        id_animal = Animals.create_animal(name, center, species, age, price, description)
        seng_message_to_log("POST", "/animals", kwargs['id'], "animal", str(id_animal))
        return {'res': "Animal was created"}, 200
    except Exception:
        traceback.print_exc()
        return {'res': f"No such species '{species}' exist, please, create it firstly"}, 401


@app.route('/species', methods=["POST"])
@token_required
@schema_validator_catcher
def register_species(**kwargs):

    get_request = request.get_json()
    jsonschema.validate(get_request, request_schemas.register_species_schema)
    name = str(get_request['name'])
    description = str(get_request['description'])
    price = str(get_request['price'])

    id_species = Species.create_cpecies(name, description, price)
    seng_message_to_log("POST", "/species", kwargs['id'], "species", str(id_species))

    return {'res': "Species was successfully registered"}, 200


@app.route('/animals/<int:animal_id>', methods=["PUT"])
@token_required
@schema_validator_catcher
def replace_animal(animal_id, **kwargs):

    get_request = request.get_json()
    jsonschema.validate(get_request, request_schemas.register_update_animal_schema)
    name, center, species, age, price, description = unwrap_data_from_animal_request(get_request)

    Animals.update_animal(animal_id, name, center, species, description, age, price)
    seng_message_to_log("PUT", f"/animals/{animal_id}", kwargs['id'], "animal", str(animal_id))

    return {'res': "Animal was successfully updated"}, 200


@app.route('/animals/<int:animal_id>', methods=["DELETE"])
@token_required
def delete_animal(animal_id, **kwargs):
    try:
        Animals.delete_animal(animal_id, kwargs['login'])
        seng_message_to_log("DELETE", f"/animals/{animal_id}", kwargs['id'], "animal", str(animal_id))
        return {'res': "Animal was deleted"}, 200
    except:
        traceback.print_exc()
        return {'res': "This center is not owner of this animal"}, 400


if __name__ == '__main__':
    app.run(port="8081")
