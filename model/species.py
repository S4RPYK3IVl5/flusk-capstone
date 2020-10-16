from sqlalchemy import func

from settings import db


class Species(db.Model):

    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    animals = db.relationship("Animals")

    def create_cpecies(name, description, price):
        new_species = Species(name=name, description=description, price=price)
        db.session.add(new_species)
        db.session.commit()


    def get_all_species():
        res = Species.query.with_entities(Species.name, func.count(Species.id)).group_by(Species.name).all()
        return [{'name': data.get('name'), 'count': data.get('count')} for data in res]

    def get_concrete_species_by_name(name):
        species = Species.query.filter_by(name=name).first()
        return species
