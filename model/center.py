from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Center(db.Model):

    __tablename__ = 'center'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)

    def crate_center(login, password, address):
        new_center = Center(id=id, login=login, password=password, address=address)
        db.session.add(new_center)
        db.session.commit()
