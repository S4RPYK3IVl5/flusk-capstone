from settings import db


class Species(db.Model):

    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    animals = db.relationship("Animals")

    def create_cpecies(name, description, price):
        new_species = Species(name=name, description=description, price=price)
        db.session.add(new_species)
        db.session.commit()

    def get_all_species():
        species = Species.query.all()
        return [f"{data.id} - {data.name} - {len(data.animals)}" for data in species]

    def get_concrete_species_by_id(id):
        specie = Species.query.filter_by(id=id).first()
        return f"{specie.name} - {len(specie.animals)}"

    def get_concrete_species_by_name(name):
        specie = Species.query.filter_by(name=name).first()
        return specie
