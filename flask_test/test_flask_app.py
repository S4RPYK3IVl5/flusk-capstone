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


def test_empty_bd(client):
    res: Response = client.get('/animals')
    assert "200 OK" == res.status
    assert b"animals" in res.data
    assert len(json.loads(res.data)['animals']) == 0
