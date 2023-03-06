from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
login_manager=LoginManager()
moment=Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    with app.app_context():
        from application.main import main_bp
        app.register_blueprint(main_bp)

        from application.api.v1 import api_bp
        app.register_blueprint(api_bp)

        from application.auth import auth_bp
        app.register_blueprint(auth_bp)

        db.create_all()
        return app
