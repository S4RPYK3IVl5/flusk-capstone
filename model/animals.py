from model.center import Center
from model.species import Species
from settings import db


class Animals(db.Model):

    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    description = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)

    def json(self):
        return {'id': self.id, 'name': self.name, 'center_id': self.center_id, 'species': self.species_id,
                'description': self.description, 'age': self.age, 'price': self.price}

    def create_animal(name, center, species_name, age, price=None, description=None):
        center_from_db = Center.get_center_by_login(center).id
        species_from_db = Species.get_concrete_species_by_name(species_name).id
        if not species_from_db:
            raise Exception()
        new_animal = Animals(name=name, center_id=center_from_db,
                             species_id=species_from_db, age=age, price=price, description=description)
        db.session.add(new_animal)
        db.session.commit()

    def get_all_animals():
        return [Animals.json(animal) for animal in Animals.query.all()]

    def get_certain_animal(id):
        return Animals.json(Animals.query.filter_by(id=id).first())

    def get_all_animals_from_center(center_id):
        return [Animals.json(animal) for animal in Animals.query.filter_by(center_id=center_id)]

    def get_all_animals_with_species(species_id):
        return [Animals.json(animal) for animal in Animals.query.filter_by(species_id=species_id)]

    def update_animal(id, name, center_login, species_name, description, age, price):
        existing_animal = Animals.query.filter_by(id=id).first()

        existing_animal.name = name
        existing_animal.center_id = Center.get_center_by_login(center_login).id
        existing_animal.species_id = Species.get_concrete_species_by_name(species_name).id
        existing_animal.description = description
        existing_animal.age = age
        existing_animal.price = price

        db.session.commit()

    def delete_animal(id, center_login):
        on_delete = Animals.query.filter_by(id=id).first()
        if on_delete.center_id == Center.get_center_by_login(center_login).id:
            db.session.delete(on_delete)
            db.session.commit()
        else:
            raise Exception()
