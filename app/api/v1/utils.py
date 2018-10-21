import re
from flask import make_response, jsonify, abort

from .models import users, products


class ValidateUser:
    def __init__(self, data):
        self.username = data['username']
        self.password = data['password']
        self.role = data['role']

    def validate_user_details(self):
        if self.username == "":
            Message = "Username is missing"
            abort(400, Message)
        if self.password == "":
            Message = "Password is missing"
            abort(400, Message)
        if self.role == "":
            Message = "Role is missing"
            abort(400, Message)
        for user in users:
            if self.username == user["username"]:
                Message = "Username '" + self.username + "' already taken"
                abort(406, Message)
        if type(self.username) != str:
            Message = "Username must be a string"
            abort(400, Message)
        if type(self.password) != str:
            Message = "Password must be a string"
            abort(400, Message)
        if type(self.role) != str:
            Message = "Role must be a string"
            abort(400, Message)
        if self.role != 'admin' or self.role != 'attendant':
            Message = 'Role must be either admin or attendant'
        if len(self.password) <= 6 or len(self.password) > 12:
            Message = "Password must be at least 6 and at most 10 ch long"
            abort(400, Message)
        elif not any(char.isdigit() for char in self.password):
            Message = "Password must have a digit"
            abort(400, Message)
        elif not any(char.isupper() for char in self.password):
            Message = "Password must have an upper case character"
            abort(400, Message)
        elif not any(char.islower() for char in self.password):
            Message = "Password must have a lower case character"
            abort(400, Message)
        elif not re.search("[#@$]", self.password):
            Message = "Password must have one of the special charater [#@$]"
            abort(400, Message)


class ValidateProduct():
    def __init__(self, data):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']

    def validate_product_details(self):
        for product in products:
            if product['title'] == self.title:
                Message = "Product: '" + self.title + "' already exists"
                abort(406, Message)

        if type(self.title) != str:
            Message = "Product title must be a string"
            abort(400, Message)

        if type(self.category) != str:
            Message = "Product Category must be a string"
            abort(400, Message)

        if type(self.description) != str:
            Message = "Product Description must be a string"
            abort(400, Message)

        if type(self.quantity) != int:
            Message = "Product quantity price must be a real number"
            abort(400, Message)
        if self.quantity < 0:
            Message = "Product Quantity should be a positive value value"
            abort(400, Message)

        if type(self.price) != float:
            Message = "Product price must be of the format 00.00"
            abort(400, Message)
        if self.price < 0:
            Message = "Product price should be a positive value"
            abort(400, Message)

        if type(self.lower_inventory) != int:
            Message = "Product lower inventory must be a real number"
            abort(400, Message)
        if self.lower_inventory < 0:
            Message = "Product price should be a positive value"
            abort(400, Message)
        if self.lower_inventory > self.quantity:
            Message = "Lower inventory should be less than the quantity"
            abort(400, Message)
