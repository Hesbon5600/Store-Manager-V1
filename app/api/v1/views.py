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


class Product(Resource):

    # Get all products
    @token_required
    def get(current_user, self):
        if current_user:
            if len(products) < 1:
                response = make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "No avilable products"
                }), 404)
            else:
                response = make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Success",
                    'My products': products
                }), 200)
        else:
            response = make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be logged in"
            }), 401)
        return response

    @token_required
    def post(current_user, self):
        data = request.get_json()

        # current_user = data['current_user
        if current_user and current_user['role'] != "admin":
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "You must be an admin"
            }), 401)
        if current_user and current_user['role'] == "admin":
            valid_product = ValidateProduct(data)
            valid_product.validate_product_details()
            product = PostProduct(data)
            product.save_product()
            return make_response(jsonify({
                'Status': 'Ok',
                'Message': "Product created Successfully",
                'My Products': products
            }), 201)


class SingleProduct(Resource):
    # Get a single product
    @token_required
    def get(current_user, self, productID):
        if current_user:
            for product in products:
                if product['id'] == int(productID):
                    return make_response(jsonify({
                        'Status': 'Ok',
                        'Message': "Success",
                        'My product': product
                    }), 200)

            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No such product"
            }), 404)


class Sale(Resource):
    # Get all sale entries
    @token_required
    def get(current_user, self):
        if current_user['role'] == "admin":
            if len(sales) > 0:
                response = make_response(jsonify({
                    'Status': 'Ok',
                    'Message': "Success",
                    'My Sale': sales
                }), 200)
            else:
                response = make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "No sales made"
                }), 404)
            return response

        return make_response(jsonify({
            'Status': 'Failed',
            'Message': "You must be an admin"
        }), 403)

    # Make a sales
    @token_required
    def post(current_user, self):
        total = 0
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "No data posted"
                                         }), 400)
        id = data['product_id']
        if current_user['role'] == 'attendant':
            for product in products:
                if product['quantity'] > 0:
                    if product['id'] == id:
                        attendant_id = current_user['id']
                        sale = {
                            'sale_id': len(sales) + 1,
                            'attendant_id': attendant_id,
                            'product': product
                        }
                        post_sale = SaveSale(sale)
                        post_sale.save_sale()
                        product['quantity'] = product['quantity'] - 1
                        for sale in sales:
                            if product['id'] in sale.values():
                                total = total + int(product['price'])
                        return make_response(jsonify({
                            'Status': 'Ok',
                            'Message': "Success",
                            'My Sales': sales,
                            "Total": total
                        }), 201)
                    else:
                        return make_response(jsonify({
                            'Status': 'Failed',
                            'Message': "product does not exist"
                        }), 404)
                else:
                    return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "No more products to sell"
                                         }), 404)
        else:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "You must be an attendant"
                                         }), 403)


class SingleSale(Resource):
    @token_required
    def get(current_user, self, saleID):
        for sale in sales:
            if current_user['id'] == sale['attendant_id'] or current_user['role'] == 'admin':
                if int(saleID) == sale['sale_id']:
                    response = make_response(jsonify({
                        'Status': 'Ok',
                        'Message': "Success",
                        'Sale': sale
                    }), 200)

                else:
                    response = make_response(jsonify({
                        'Status': 'Failed',
                        'Message': "No avilable sales"
                    }), 404)
                return response
            else:
                return make_response(jsonify({
                    'Status': 'Failed',
                    'Message': "You cannor access this sale record"
                }), 401)


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                'Status': 'Failed',
                'Message': "No signup data provided"
            }), 400)

        validate = ValidateUser(data)
        validate.validate_user_details()
        user = SaveUser(data)
        user.save_user()
        for user in users:
            username = user['username']
            role = user['role']
 
            return make_response(jsonify({
                'Status': 'Ok',
                'Message': "User '" + username + "' successfully registered as '" + role,
            }), 201)


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
            if user['username'] == username and check_password_hash(user["password"],
                                                                    password):
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
