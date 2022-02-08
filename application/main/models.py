from application import db
from flask import jsonify


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    @staticmethod
    def from_json(json_user):
        return User(name=json_user.get("name"),email=json_user.get("email"))