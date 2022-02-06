from flask import Flask
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    with app.app_context():
        from .main import main_bp
        app.register_blueprint(main_bp)

        return app