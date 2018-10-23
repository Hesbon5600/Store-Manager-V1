import datetime
from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from instance.config import app_config
import jwt
from .models import *
from .utils import *


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # data = request.get_json()
        token = None
        current_user = None
        if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
        if not token:
            return make_response(jsonify({
                'Message': 'Token is missing, You must login first'
                }), 401)
        try:
            data = jwt.decode(token, app_config['development'].SECRET_KEY)
            for user in users:
                if user['username'] == data['username']:
                    current_user = user
        except:
            return make_response(jsonify({'Message': 'Token is invalid'}),
                                          403)
        return f(current_user, *args, **kwargs)
    return decorated


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data['username'] or not data['password'] or not data['role']:
            response = make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "You must provide a username, password and role"
                    }), 400)

        else:
            username = data['username']
            password = data['password']
            role = data['role']
            validate = Validate(username, password, role)
            validate.validate_user_details()
            user = SaveUser(username, password, role)
            user.save_user()
            response = make_response(jsonify({
                'Status': 'Ok',
                'Message': "User added successfully",
                'Users': users
            }), 201)
        return response


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        if not data or not username or not password:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "Login required"
                                         }), 400)

        for user in users:
            if user['username'] == username and user['password'] == password:
                token = jwt.encode({'username': user['username'],
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=3000)},
                                    app_config['development'].SECRET_KEY)
                return make_response(jsonify({
                                             'token': token.decode('UTF-8')
                                             }), 200)

        return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No such user found. Check your login credentials"
                }), 404)


class Product(Resource):
    @token_required
    def post(current_user, self):
        data = request.get_json()
        title = data['title']
        category = data['category']
        description = data['description']
        quantity = data['quantity']
        price = data['price']
        lower_inventory = data['lower_inventory']

        # current_user = data['current_user
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                            'Status': 'Failed',
                            'Message': "You must be an admin"
                          }), 401)
        if current_user and current_user['role'] == "admin":
            product = PostProduct(
                title, category, description, quantity, price, lower_inventory)
            product.save_product()
            return make_response(jsonify({
                'Status': 'Ok',
                'Message': "Product created Successfully",
                'My Products': products
            }), 201)


