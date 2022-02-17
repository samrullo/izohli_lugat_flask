from application import db, login_manager
from flask_login import UserMixin
from application.main.models import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(UserMixin, BaseModel, BaseUser, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200))
    name = db.Column(db.String(200))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
