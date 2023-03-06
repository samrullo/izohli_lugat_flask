import os
import pathlib
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    name = "izohli_lugat"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION')) or 3600    


class DevelopmentConfig(Config):
    name = "development mode"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "application",
                                                                                                "data", "dev.sqlite")
    ELASTICSEARCH_DOMAIN=os.environ.get('ELASTICSEARCH_DOMAIN') or "localhost:9200"


class ProductionConfig(Config):
    name = "production mode"
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, "data",
                                                                                                 "prod.sqlite")
    ELASTICSEARCH_DOMAIN=os.environ.get('ELASTICSEARCH_DOMAIN') or "localhost:9200"


config = {"production": "config.ProductionConfig",
          "development": "config.DevelopmentConfig"}
