from settings import db


class AccessRequest(db.Model):

    __tablename__ = 'access_request'
    center_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def add_record(center_id, timestamp):
        new_record = AccessRequest(center_id=center_id, timestamp=timestamp)
        db.session.add(new_record)
        db.session.commit()
