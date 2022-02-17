from application import db
import datetime


class BaseModel:
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.datetime.now)


class Product(BaseModel, db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

    def to_json(self):
        return {"id": self.id, "name": self.name, "price": self.price, "created_at": self.created_at,
                "modified_at": self.modified_at}

    @staticmethod
    def from_json(json_product):
        return Product(name=json_product.get("name"), price=json_product.get("price"))


class Category(BaseModel, db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)