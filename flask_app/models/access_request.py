from flask_app.config.settings import db
from flask_app.models.center import Center


class AccessRequest(db.Model):
    """
    The AccessRequest model used for recording access request to service via 'login'
    """

    __tablename__ = 'access_request'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    timestamp = db.Column(db.DateTime, nullable=False)

    def register_access_request(center_login, timestamp):
        """
        Save AccessRequest record to DB
        :param center_login:
            The login of center, which requested an access to service
        :param timestamp:
            Time, when access have been requested
        :return:
        """
        center_from_db_id = Center.get_center_by_login(center_login).id
        new_access_request = AccessRequest(center_id=center_from_db_id, timestamp=timestamp)
        db.session.add(new_access_request)
        db.session.commit()
