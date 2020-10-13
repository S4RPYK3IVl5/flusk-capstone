from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Species(db.Model):

    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

