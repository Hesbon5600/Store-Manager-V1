import datetime
from functools import wraps
from flask import Flask, jsonify, make_response, request
from flask_restful import Resource, Api
from instance.config import app_config
import jwt
from .models import *
from .utils import *


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

