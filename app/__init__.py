from flask import Flask
from app.admin import initialize_admin
from app.jwt import initialize_jwt
from app.db import initialize_db
from app.utils.scripts import load_subjects_from_csv

def create_app():
    app = Flask(__name__)

    from app.api import api_bp
    # from app.views.routes import web_bp
    from app.auth.routes import auth_bp
    # Configuración de la base de datos MongoDB
    with app.app_context():
        initialize_db(app)
        initialize_admin(app)
        initialize_jwt(app)

    load_subjects_from_csv()
    # app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)


# Setup the Flask-JWT-Extended extension

    return app

