from flask import Flask
from config import config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)

    with app.app_context():
        from application.main import main_bp
        app.register_blueprint(main_bp)

        from application.api.v1 import api_bp
        app.register_blueprint(api_bp)

        db.create_all()
        return app
