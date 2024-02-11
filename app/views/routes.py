from flask import render_template, Blueprint
from flask_jwt_extended import jwt_required


web_bp = Blueprint('web', __name__, template_folder='templates')

@web_bp.route('/')
@jwt_required(optional=True)
def index():
    return render_template('index.html')

@web_bp.route('/register')
def register():
    return render_template('register.html')

@web_bp.route('/login')
def login():
    return render_template('login.html')

