from flask_app.config.settings import db


class Center(db.Model):
    """
        The Center model used for operating with 'center' table in database
    """

    __tablename__ = 'center'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), unique=True, nullable=False)
    animals = db.relationship("Animals")

    def _format_model(self):
        """
        Create representation for Center
        :return:
            :type str
                The representation of Center
        """
        return f"{self.login} - {self.id}"

    @classmethod
    def create_center(cls, login, password, address):
        """
        Create and save Center instance to db
        :param login:
            :type str
                Login for center
        :param password:
            :type str
                Password for center
        :param address:
            :type str
                Address for center
        :return:
            :type int
                Id of created center
        """
        new_center = Center(login=login, password=password, address=address)
        db.session.add(new_center)
        return new_center.id

    @classmethod
    def is_center_exist(cls, login, password):
        """
        Check for the presence of the center
        :param login:
            :type str
                Login for center
        :param password:
            :type str
                Password for center
        :return:
            :type bool
                Indicator of the presence of the centers
        """
        center = Center.query.filter_by(login=login).filter_by(password=password).first()
        if center:
            return True
        else:
            return False

    @classmethod
    def get_all_centers(cls):
        """
        Return all Center, stored in db
        :return:
            :type list
                The list of all stored centers
        """
        return [Center._format_model(center) for center in Center.query.all()]

    @classmethod
    def get_center_by_login(cls, login):
        """
        Return a certain Center by login
        :param login:
            :type str
                The login of Center
        :return:
            :type Center
                The instance of Center
        """
        center = Center.query.filter_by(login=login).first()
        return center

    @classmethod
    def get_certain_center(cls, id):
        """
        Return a certain Center by id
        :param id:
            :type int
                The id of Center
        :return:
            :type Center
                The instance of Center
        """
        center = Center.query.filter_by(id=id).first()
        center_id = center.id
        center_login = center.login
        return [f"{animal.name} - {center_id} - {center_login}"
                for animal in center.animals]
