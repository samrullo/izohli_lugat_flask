from application.api.v1 import api_bp
from flask import jsonify, request, current_app
from application.main.models import User
from application import db
import json


@api_bp.route("/users")
def users():
    users = User.query.all()
    users = [user.to_json() for user in users]
    return jsonify({"users": users})


@api_bp.route("/users/<user_id>")
def user(user_id):
    user = User.query.get(user_id)
    return jsonify({"user": user.to_json()})

def log_request_data(request):
    if request.is_json:
        current_app.logger.info("request.is_json is True")
        data = request.json
        current_app.logger.info(f"type of data {type(data)}")
        current_app.logger.info(f"str data keys after dumping to json : {json.dumps(data)}")
    else:
        current_app.logger.info(f"request data is not json {request}")


@api_bp.route("/users", methods=["POST"])
def new_user():
    log_request_data(request)
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())


@api_bp.route("/users", methods=["PUT"])
def update_user():
    log_request_data(request)
    user_data = request.json
    user_id = int(user_data["id"])
    user = User.query.get(user_id)
    for key in user_data.keys():
        if key != "id":
            setattr(user,key,user_data[key])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())

@api_bp.route("/users",methods=["DELETE"])
def remove_user():
    log_request_data(request)
    user_data=request.json
    user_id=int(user_data["id"])
    user=User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":f"Successfully removed {user_data['name']} {user_data['email']}"})