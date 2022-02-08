from application.api.v1 import api_bp
from flask import jsonify,request
from application.main.models import User
from application import db

@api_bp.route("/users")
def users():
    users = User.query.all()
    users=[user.to_json() for user in users]
    return jsonify({"users":users})

@api_bp.route("/users/<user_id>")
def user(user_id):
    user=User.query.get(user_id)
    return jsonify({"user":user.to_json()})

@api_bp.route("/users",methods=["POST"])
def new_user():
    user=User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())