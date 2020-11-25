import functools
from flask import Blueprint, request, jsonify, current_app, make_response
from flask_cors import cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import json

from . import db
from .models.user import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


@bp.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    name = data['name']
    email = data['email']
    password = data(request.form['password'])
    error = None

    if not name:
        error = 'Name is required'
    elif not email:
        error = 'Email is required'
    elif not password:
        error = 'Password is required'

    if error is None:
        db_user = User.objects(email=email).first()
        if db_user is not None:
            error = "Email already registered."

    if error is None:
        user = User(
            name=name,
            email=email,
            password=password
        )
        user.save()
        return "Registration successful."
    else:
        return error


@bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = json.loads(request.data)
    current_app.logger.info(data)
    email = data['email']
    password = data['password']
    error = None

    user = User.objects(email=email).first()

    if user is None:
        error = "Email not found."
    elif not check_password_hash(user['password'], password):
        error = "Incorrect password."

    if error is None:
        token = jwt.encode({
            'name': user.name,
        }, current_app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})
    else:
        return error

