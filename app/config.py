import os
from datetime import timedelta

def get_mongo_from_uri(uri):
    conn_settings = {"host": uri, 'connect': False}
    return conn_settings

class Config:
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = get_mongo_from_uri(os.getenv("DEV_MONGODB_URI"))
    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    JWT_SECRET_KEY = "DSFSDGSGDEV"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tiempo de expiración del token


class ProductionConfig(Config):
    MONGO_URI = get_mongo_from_uri(os.environ.get('PROD_MONGODB_URI'))
    SECRET_KEY = os.environ.get('PROD_SECRET_KEY')
    JWT_SECRET_KEY = "DSFSDGSGPROD"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tiempo de expiración del token
