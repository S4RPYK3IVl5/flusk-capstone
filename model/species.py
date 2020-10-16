from flask_sqlalchemy import SQLAlchemy
from app import app
from sqlalchemy import func

from model.animals import Animals

db = SQLAlchemy(app)


class Species(db.Model):

    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def create_cpecies(name, description, price):
        new_species = Species(name=name, description=description, price=price)
        db.session.add(new_species)
        db.session.commit()


    def get_all_species():
        res = Species.query.with_entities(Species.name, func.count(Species.id)).group_by(Species.name).all()
        return [{'name': data.get('name'), 'count': data.get('count')} for data in res]

    def get_concrete_species_by_name(name):
        species = Species.query.filter_by(name=name).first()
        species_id = species.id
        species_login = species.login
        return [f"{animal['name']} - {species_id} - {species_login}"
                for animal in Animals.get_all_animals_with_species(species_id)]
