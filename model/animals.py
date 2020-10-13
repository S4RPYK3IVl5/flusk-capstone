from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)


class Animals(db.Model):

    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    species = db.Column(db.Integer, db.ForeignKey('species.id'))
    description = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)
