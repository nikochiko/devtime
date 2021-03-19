from sqlalchemy import event

from app import db
from app.utils import generate_api_key


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    api_key = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return f"<User: {self.username}>"


# Events

@event.listens_for(User, "before_insert")
def receive_before_insert(_mapper, _connection, target):
    """When a new record is created, assign an api key to it"""
    if not target.api_key:
        target.api_key = generate_api_key()
