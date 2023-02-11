import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    name = "flask_app"

    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION')) or 3600


class DevelopmentConfig(Config):
    name = "development mode"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "application",
                                                                                                "data", "dev.sqlite")


class ProductionConfig(Config):
    name = "production mode"
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "data",
                                                                                                 "prod.sqlite")


config = {"production": "config.ProductionConfig",
          "development": "config.DevelopmentConfig"}
