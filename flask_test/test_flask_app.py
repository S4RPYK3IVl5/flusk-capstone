import os
import tempfile
from flask_app.config.settings import app, db

import pytest


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_empty_bd(client):
    res = client.get('/animals')
    print(res.data)
    assert "Center was successfully registered" == res.data


# def test_register_functionality(client):
#     res = client.post('/register', data=dict(
#         login="Super puper center 2",
#         password="1",
#         address="magic address 1"
#     ))
#     print(res.data)
#     assert "Center was successfully registered" == res.data
