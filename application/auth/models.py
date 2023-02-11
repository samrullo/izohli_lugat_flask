from application import db, login_manager
from flask_login import UserMixin
from flask import current_app, jsonify
from application.main.models import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer


class BaseUser:
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not directly accessible")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_auth_token(id, expiration):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps({"id": id, 'expiration': expiration})

    @staticmethod
    def verify_auth_token(token, expiration):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id_dict = s.loads(token, max_age=expiration)
            current_app.logger.info(f"decoded user_id_dict is {user_id_dict}")
        except Exception as e:
            current_app.logger.info(f"something went wrong : {e}")
            return None
        return User.query.get(user_id_dict["id"])


class User(UserMixin, BaseModel, BaseUser, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    name = db.Column(db.String(200))

    def to_json(self):
        return {"id": self.id, "email": self.email, "name": self.name, "created_at": self.created_at,
                        "modified_at": self.modified_at}

    @staticmethod
    def from_json(json_user):
        return User(email=json_user.get("email"), name=json_user.get("name"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
