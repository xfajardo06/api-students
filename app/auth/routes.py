from flask import request, Blueprint
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from pydantic import ValidationError
from app.auth.schemas import UserLoginSchema, UserRegisterSchema

# Models
from app.models.users import User

# Utilidades
import app.utils.responses as resp
from app.utils.responses import response_with

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@auth_bp.route('/register/', methods=['POST'])
def register():
    data = request.json

    try:
        request_register = UserRegisterSchema(**data)
    except ValidationError as e:
        return response_with(
            response=resp.BAD_REQUEST_SCHEMA,
            error = e.errors()
        )

    if User.objects(email=request_register.email).first():
        return response_with(response=resp.BAD_REQUEST_400, error="El usuario ya existe")

    user = User()
    user.email = request_register.email
    user.name = request_register.name
    user.set_password(request_register.password)
    user.save()
    return response_with(response=resp.SUCCESS_200, message="Usuario creado exitosamente")

# Ruta para la autenticación y generación del token JWT
@auth_bp.route('/login', methods=['POST'])
@auth_bp.route('/login/', methods=['POST'])
def login_user():
    data = request.json

    try:
        request_login = UserLoginSchema(**data)
    except ValidationError as e:
        return response_with(
            response=resp.BAD_REQUEST_SCHEMA,
            error = e.errors()
        )

    # Verifica las credenciales del usuario
    user = User.objects(email=request_login.email).first()

    if user and user.check_password(request_login.password):
        access_token = create_access_token(identity=str(user.id))
        return response_with(response=resp.SUCCESS_200, data={"access_token": access_token})
    else:
        return response_with(response=resp.BAD_REQUEST_400, error="Credenciales invalidas.")


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Elimina el token del cliente
    unset_jwt_cookies()

    return response_with(response=resp.SUCCESS_200)
