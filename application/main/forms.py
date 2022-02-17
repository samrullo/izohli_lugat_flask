from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField

class ProductForm(FlaskForm):
    name=StringField("Name")
    price=IntegerField("Price")
    submit=SubmitField("Submit")

    def __str__(self):
        return f"{self.name.data} {self.price.data}"

class CategoryForm(FlaskForm):
    name=StringField("Category Name")
    submit = SubmitField("Submit")