from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, unset_jwt_cookies, jwt_required
from pydantic import ValidationError
from app.api.auth.schemas import UserLoginSchema, UserRegisterSchema

# Models
from app.models.users import User

# Utilidades
import app.utils.responses as resp
from app.utils.responses import response_with

api = Namespace(
    name = 'auth',
    description="API: Autenticación",
)

@api.route('/register')
class Register(Resource):
    def post(self):
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
@api.route('/login')
class LoginUser(Resource):
    def post(self):
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


@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        # Elimina el token del cliente
        unset_jwt_cookies()

        return response_with(response=resp.SUCCESS_200)
