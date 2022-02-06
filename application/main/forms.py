from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

class RegisterForm(FlaskForm):
    name=StringField("Name")
    email=StringField("Email")
    submit=SubmitField("Submit")

    def __str__(self):
        return f"{self.name.data} {self.email.data}"