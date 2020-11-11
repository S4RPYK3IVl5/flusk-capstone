from flask_app.models.center import Center
from flask_app.models.species import Species
from flask_app.config.settings import db
from flask_app.utils import NoAccessException, SpeciesDoesNotExistException


class Animals(db.Model):
    """
    The Animals model used for operating with 'animal' table in database
    """
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'))
    description = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)

    def json(self):
        """
        This function creates dict of animal instance for representation
        :return:
            :type dict
                The representation of animal
        """
        return {'id': self.id, 'name': self.name, 'center_id': self.center_id, 'species': self.species_id,
                'description': self.description, 'age': self.age, 'price': self.price}

    @classmethod
    def create_animal(cls, name, center, species_name, age, price=None, description=None):
        """
        Create animal instance to save it in db
        :param name:
            :type str
                Name of animal
        :param center:
            :type str
                Login of center
        :param species_name:
            :type str
                Name of specie
        :param age:
            :type str
                Age of animal
        :param price:
            :type str
                Price of animal
        :param description:
            :type str
                Description of animal
        :return:
            :type int
                The id of created animal
        """
        center_from_db = Center.get_center_by_login(center).id
        species_from_db = Species.get_concrete_species_by_name(species_name).id
        if not species_from_db:
            raise SpeciesDoesNotExistException()
        new_animal = Animals(name=name, center_id=center_from_db,
                             species_id=species_from_db, age=age, price=price, description=description)
        db.session.add(new_animal)
        return new_animal.id

    @classmethod
    def get_all_animals(cls):
        """
        Return all Animals, stored in db
        :return:
            :type list
                The list of all stored Animals
        """
        return [Animals.json(animal) for animal in Animals.query.all()]

    @classmethod
    def get_certain_animal(cls, id):
        """
        Return a certain Animal by id
        :param id:
            :type int
                The id of Animal
        :return:
            :type Animals
                The instance of Animal
        """
        return Animals.json(Animals.query.filter_by(id=id).first())

    @classmethod
    def update_animal(cls, id, name, center_login, species_name, description, age, price):
        """
        Update animal by specific id
        :param id:
            :type int
                Name of animal
        :param name:
            :type str
                Name of animal
        :param center_login:
            :type str
                Login of center
        :param species_name:
            :type str
                Name of specie
        :param age:
            :type str
                Age of animal
        :param price:
            :type str
                Price of animal
        :param description:
            :type str
                Description of animal
        :return:
            :type int
                The id of updated animal
        """
        existing_animal = Animals.query.filter_by(id=id).first()

        existing_animal.name = name
        existing_animal.center_id = Center.get_center_by_login(center_login).id
        existing_animal.species_id = Species.get_concrete_species_by_name(species_name).id
        existing_animal.description = description
        existing_animal.age = age
        existing_animal.price = price

        return existing_animal.id

    @classmethod
    def delete_animal(cls, id, center_login):
        """
        Delete animal from DB
        :param id:
            :type int:
                The id of animal
        :param center_login:
            :type str
                The login of center
        """
        on_delete = Animals.query.filter_by(id=id).first()
        if on_delete.center_id == Center.get_center_by_login(center_login).id:
            db.session.delete(on_delete)
        else:
            raise NoAccessException()
