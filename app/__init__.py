import os
from dotenv import load_dotenv

from flask import Flask
from app.admin import initialize_admin
from app.jwt import initialize_jwt
from app.db import initialize_db
from app.utils.scripts import load_subjects_from_csv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app_settings = os.environ.get('APP_SETTINGS', 'app.config.DevelopmentConfig')
    app.config.from_object(app_settings)
    app.config.from_pyfile('config.py', silent=True)
    print(app.config)
    from app.api import api_bp

    with app.app_context():
        # Configuración de la base de datos MongoDB
        initialize_db(app)
        # Flask admin
        initialize_admin(app)
        # Flask JWT
        initialize_jwt(app)

    load_subjects_from_csv()
    app.register_blueprint(api_bp)

    return app

