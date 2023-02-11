from flask_httpauth import HTTPBasicAuth
from application.auth.models import User
from flask import g,current_app
from .error import unauthorized
auth=HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token== "":
        return False
    if password=="":
        current_app.logger.info(f"token was used when accessing API : {email_or_token}")
        g.current_user=User.verify_auth_token(email_or_token,current_app.config["TOKEN_EXPIRATION"])
        current_app.logger.info(f"g.current_user is {g.current_user}")
        g.token_used=True
        return g.current_user is not None
    current_app.logger.info(f"email and password was sent : {email_or_token}, {password}")
    user=User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user=user
    g.token_used=False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized("Invalid Credentials")