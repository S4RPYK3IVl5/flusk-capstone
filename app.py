import datetime

from model.animals import Animals
from model.center import Center
from model.species import Species
from settings import app
from flask import request, Response, jsonify
import jwt

APPLICATION_JSON = "application/json"


@app.route("/login", methods=["POST"])
def login_in():

    get_request = request.get_json()
    login = str(get_request['login'])
    password = str(get_request['password'])

    if Center.is_center_exist(login, password):
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm="HS256")
        return token
    else:
        return Response('', 401, mimetype=APPLICATION_JSON)


@app.route('/animals', methods=["GET"])
def get_all_animals():
    return Animals.get_all_animals()


@app.route('/animals/<int:id>', methods=["GET"])
def get_certain_animal(id):
    return Animals.get_certain_animal(id)


@app.route('/centers', methods=["GET"])
def get_all_centers():
    return Center.get_all_centers()


@app.route('/centers/<int:id>', methods=["GET"])
def get_certain_center(id):
    return Center.get_certain_center(id)


@app.route('/species ', methods=["GET"])
def get_all_species():
    return Species.get_all_species()


@app.route('/species/<int:id>', methods=["GET"])
def get_concrete_species(id):
    return Species.get_concrete_species(id)


if __name__ == '__main__':
    app.run(port="8081")
