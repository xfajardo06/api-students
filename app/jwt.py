from flask_jwt_extended import JWTManager

from app.utils.responses import response_with
import app.utils.responses as resp

jwt = JWTManager()

def initialize_jwt(app):
    # Setup the Flask-JWT-Extended extension
    jwt.init_app(app)

@jwt.expired_token_loader
def expired_token_callback(header, data):
    return response_with(
            response=resp.UNAUTHORIZED_401,
            error ="El token ha expirado"
        )

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return response_with(
            response=resp.UNAUTHORIZED_401,
            error ="Token inválido"
        )

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return response_with(
            response=resp.UNAUTHORIZED_401,
            error ="No ha proporcionado un token"
    )