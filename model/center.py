from flask_sqlalchemy import SQLAlchemy
from app import app
from model.animals import Animals

db = SQLAlchemy(app)


class Center(db.Model):

    __tablename__ = 'center'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)

    def _format_model(self):
        return f"{self.login} - {self.id}"

    def crate_center(login, password, address):
        new_center = Center(id=id, login=login, password=password, address=address)
        db.session.add(new_center)
        db.session.commit()

    def is_center_exist(login, password):
        center = Center.query.filter_by(login=login).filter_by(password=password).first()
        if center:
            return True
        else:
            return False

    def get_all_centers():
        return [Center._format_model(center) for center in Center.query.all()]

    def get_certain_center(id):
        center = Center.query.filter_by(id=id).first()
        center_id = center.id
        center_login = center.login
        return [f"{animal['name']} - {center_id} - {center_login}"
                for animal in Animals.get_all_animals_from_center(center_id)]

