from flask_app.config.settings import db
from flask_app.utils import SpeciesDoesNotExistException


class Species(db.Model):

    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    animals = db.relationship("Animals")

    @classmethod
    def create_species(cls, name, description, price):
        """
        Create Species instance and save it to db
        :param name:
            :type str
                The name of a Species
        :param description:
            :type str
                The description of a Species
        :param price:
            :type int
                The price of a Species
        :return:
            :type int
                Id of created Species
        """
        new_species = Species(name=name, description=description, price=price)
        db.session.add(new_species)

    @classmethod
    def get_all_species(cls):
        """
        Return all Species, stored in db
        :return:
            :type list
                The list of all stored species
        """
        species = Species.query.all()
        return [f"{data.id} - {data.name} - {len(data.animals)}" for data in species]

    @classmethod
    def get_concrete_species_by_id(cls, id):
        """
        Return specific Species by id
        :param id:
            :type int
                The id of a Species
        :return:
            :type str
                The string representation of a Specie
        """
        specie = Species.query.filter_by(id=id).first()
        return f"{specie.name} - {len(specie.animals)}"

    @classmethod
    def get_concrete_species_by_name(cls, name):
        """
        Return specific Species by name
        :param name:
            :type str
                The name of a Species
        :return:
            :type str
                The instance of Species
        """
        specie = Species.query.filter_by(name=name).first()
        if not specie:
            raise SpeciesDoesNotExistException(f"No such center with name: {name}")
        return specie
