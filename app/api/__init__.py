from flask import Blueprint
from flask_restx import Api

# Importar las rutas y registrarlas
from .subjects import api as api_subjects
from .students import api as api_students
from .auth import api as api_auth

api_bp = Blueprint('api', __name__)

# Crear un Blueprint para el módulo api
api = Api(
    app=api_bp, prefix='/api/v1', version='1.0',
    title='API Gestion de Calificaciones de Universidad Nacional',
    description=''
)
# Registrar las rutas en el Blueprint
api.add_namespace(api_auth)
api.add_namespace(api_students)
api.add_namespace(api_subjects)
