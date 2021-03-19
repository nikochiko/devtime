from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    api_key = db.Column(db.String(255), index=True, unique=True)

    def __repr__(self):
        return f"<User: {self.username}>"
