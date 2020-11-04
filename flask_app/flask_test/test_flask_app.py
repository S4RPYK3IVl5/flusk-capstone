import json
import os
import tempfile

from flask.wrappers import Response

from flask_app.app import app
from flask_app.config.settings import db

import pytest


@pytest.fixture
def client():
    db_fd, temp_url = tempfile.mkstemp()
    temp_url_with_db = temp_url + ".db"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + temp_url_with_db

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(temp_url_with_db)


def registration_center(client, login, password, address):
    sent = {
        'login': login,
        'password': password,
        'address': address
    }
    result = client.post(
        '/register',
        data=sent
    )
    return result


def log_in(client, login, password):
    sent = {
        'login': login,
        'password': password
    }
    result = client.post(
        '/login',
        data=sent
    )
    return result


def create_species(client, name, token, price, description):
    sent = {
        'name': name,
        'description': description,
        'price': price,
        'token': token
    }
    result = client.post(
        '/species',
        data=sent
    )
    return result


def create_animal(client, token, name,  center, species, age, price=None, description=None):
    sent = {
        'token': token,
        "name": name,
        'center': center,
        'species': species,
        'age': age,
        'price': price,
        'description': description
    }
    result = client.post(
        '/animals',
        data=sent
    )
    return result


def test_empty_bd(client):
    res: Response = client.get('/animals')
    assert "200 OK" == res.status
    assert b"animals" in res.data
    assert len(json.loads(res.data)['animals']) == 0


def test_registration(client):
    res = registration_center(client, "test_login", "test_password", "test_address")
    assert "200 OK" == res.status


def test_log_in(client):
    registration_center(client, "test_login", "test_password", "test_address")
    res = log_in(client, "test_login", "test_password")
    assert "200 OK" == res.status
    assert b"token" in res.data


def test_create_species(client):
    registration_center(client, "test_login", "test_password", "test_address")
    res = log_in(client, "test_login", "test_password")
    res_json = json.loads(res.data)
    to_assert = create_species(client, "test_name", res_json['token'], "200", "test_description")
    assert "200 OK" == to_assert.status
    species = client.get("/species/1")
    species_json = json.loads(species.data)
    assert "specie" in species_json
    assert "test_name - 0" == species_json['specie']


def test_create_animal(client):
    registration_center(client, "test_login", "test_password", "test_address")
    res = log_in(client, "test_login", "test_password")
    token = json.loads(res.data)['token']
    create_species(client, "test_name", token, "200", "test_description")
    res = create_animal(client, token, "Barsic", "test_login", "test_name", 4, 200)
    assert "200 OK" == res.status
    animal = client.get("/animals/1")
    animal_json = json.loads(animal.data)
    assert "animal" in animal_json
    assert animal_json['animal']['name'] == "Barsic"


def test_delete_animal(client):
    registration_center(client, "test_login", "test_password", "test_address")
    registration_center(client, "test_login_1", "test_password_1", "test_addres_1")
    log_in_center_1 = log_in(client, "test_login", "test_password")
    log_in_center_2 = log_in(client, "test_login_1", "test_password_1")
    token_1 = json.loads(log_in_center_1.data)['token']
    token_2 = json.loads(log_in_center_2.data)['token']

    create_species(client, "test_name", token_1, "200", "test_description")
    create_animal(client, token_1, "Barsic", "test_login", "test_name", 4, 200)

    failed_res = client.delete(
        '/animals/1',
        data={
            'token': token_2
        }
    )
    failed_res_json = json.loads(failed_res.data)
    assert "res" in failed_res_json
    assert "This center is not owner of this animal" == failed_res_json['res']

    success_res = client.delete(
        '/animals/1',
        data={
            'token': token_1
        }
    )
    success_res_json = json.loads(success_res.data)
    assert "res" in success_res_json
    assert "Animal was deleted" == success_res_json['res']
