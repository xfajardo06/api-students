# from flask import Blueprint, render_template, redirect, request, url_for
# from flask_jwt_extended import jwt_required, get_jwt_identity

# from app.models.users import User

# web_bp = Blueprint('web', __name__)

# @web_bp.route("/")
# @jwt_required(optional=True)
# def home():

#     current_user_id = get_jwt_identity()

#     return render_template('index.html')
