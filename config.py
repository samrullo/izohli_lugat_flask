import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    name = "flask_app"


class DevelopmentConfig(Config):
    name = "development mode"


class ProductionConfig(Config):
    name = "production mode"


config = {"production": "config.ProductionConfig",
          "development": "config.DevelopmentConfig"}
