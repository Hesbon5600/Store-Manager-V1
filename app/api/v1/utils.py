import re
from flask import make_response, jsonify, abort

from .models import users


class Validate:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def validate_user_details(self):
        for user in users:
            if self.username == user["username"]:
                Message = "Username already taken"
                abort(406, Message)
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
