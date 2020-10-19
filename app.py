import datetime
import traceback
from functools import wraps

from model.animals import Animals
from model.center import Center
from model.species import Species
from settings import app
from flask import request, Response, jsonify
import jwt

APPLICATION_JSON = "application/json"


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.get_json().get('token')
        if not token:
            return jsonify({"error": "You need to provide token"})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs, login=payload['login'])
        except:
            traceback.print_exc()
            return jsonify({'error': "Need a valid token to view this page"}), 401
    return wrapper


@app.route("/login", methods=["POST"])
def login_in():

    get_request = request.get_json()
    login = str(get_request['login'])
    password = str(get_request['password'])

    if Center.is_center_exist(login, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        token = jwt.encode({'exp': expiration_date, 'login': login}, app.config['SECRET_KEY'], algorithm="HS256")
        return token
    else:
        return Response('Incorrect login or password', 401, mimetype=APPLICATION_JSON)


@app.route('/animals', methods=["GET"]) #
def get_all_animals():
    return {'animals': Animals.get_all_animals()}, 200


@app.route('/animals/<int:id>', methods=["GET"]) #
def get_certain_animal(id):
    return {'animal': Animals.get_certain_animal(id)}, 200


@app.route('/centers', methods=["GET"]) #
def get_all_centers():
    return {"centers": Center.get_all_centers()}, 200


@app.route('/centers/<int:id>', methods=["GET"]) #
def get_certain_center(id):
    return {"center": Center.get_certain_center(id)}, 200


@app.route('/species', methods=["GET"]) #
def get_all_species():
    return {'species': Species.get_all_species()}, 200


@app.route('/species/<int:id>', methods=["GET"]) #
def get_concrete_species(id):
    return {'specie': Species.get_concrete_species_by_id(id)}, 200


@app.route('/register', methods=["POST"])
def register_center():

    get_request = request.get_json()
    login = str(get_request['login'])
    password = str(get_request['password'])
    address = str(get_request['address'])

    Center.create_center(login, password, address)

    return Response("Center was successfully registered", 200, mimetype=APPLICATION_JSON)


@app.route('/animals', methods=["POST"])
@token_required
def register_animal(**kwargs):

    get_request = request.get_json()
    name = str(get_request['name'])
    center = str(get_request['center'])
    species = str(get_request['species'])
    age = str(get_request['age'])
    price = str(get_request.get('price', None))
    description = str(get_request.get('description', None))

    try:
        Animals.create_animal(name, center, species, age, price, description)
        return Response("Animal was created", 200, mimetype=APPLICATION_JSON)
    except Exception:
        traceback.print_exc()
        return Response("No such species {species} exist, please, create it firstly",
                        401, mimetype=APPLICATION_JSON)


@app.route('/species', methods=["POST"])
@token_required
def register_species(**kwargs):

    get_request = request.get_json()
    name = str(get_request['name'])
    description = str(get_request['description'])
    price = str(get_request['price'])

    Species.create_cpecies(name, description, price)

    return Response("Species was successfully registered", 200, mimetype=APPLICATION_JSON)


@app.route('/animals/<int:id>', methods=["PUT"])
@token_required
def replace_animal(id, **kwargs):

    get_request = request.get_json()
    name = str(get_request['name'])
    center = str(get_request['center'])
    species = str(get_request['species'])
    age = str(get_request['age'])
    price = str(get_request.get('price', None))
    description = str(get_request.get('description', None))

    Animals.update_animal(id, name, center, species, description, age, price)

    return Response("Animal was successfully updated", 200, mimetype=APPLICATION_JSON)


@app.route('/animals/<int:id>', methods=["DELETE"])
@token_required
def delete_animal(id, **kwargs):
    try:
        Animals.delete_animal(id, kwargs['login'])
        return Response("Animal was deleted", 200)
    except:
        return Response("This center is not owner of this animal", 400)


if __name__ == '__main__':
    app.run(port="8081")
