from application.api.v1 import api_bp
from flask import jsonify, request, current_app
from application.main.models import Product
from application import db
import json


@api_bp.route("/products")
def products():
    products = Product.query.all()
    products = [product.to_json() for product in products]
    return jsonify({"products": products})


@api_bp.route("/products/<product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return jsonify({"product": product.to_json()})

def log_request_data(request):
    if request.is_json:
        current_app.logger.info("request.is_json is True")
        data = request.json
        current_app.logger.info(f"type of data {type(data)}")
        current_app.logger.info(f"str data keys after dumping to json : {json.dumps(data)}")
    else:
        current_app.logger.info(f"request data is not json {request}")


@api_bp.route("/products", methods=["POST"])
def new_product():
    log_request_data(request)
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json())


@api_bp.route("/products", methods=["PUT"])
def update_product():
    log_request_data(request)
    product_data = request.json
    product_id = int(product_data["id"])
    product = Product.query.get(product_id)
    for key in product_data.keys():
        if key != "id":
            setattr(product,key,product_data[key])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json())

@api_bp.route("/products",methods=["DELETE"])
def remove_product():
    log_request_data(request)
    product_data=request.json
    product_id=int(product_data["id"])
    product=Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message":f"Successfully removed {product_data}"})