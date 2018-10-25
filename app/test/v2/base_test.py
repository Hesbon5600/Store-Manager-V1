import unittest
import json
from app.api.v2.models import *
from app import create_app
from instance.config import app_config


class BaseTest(unittest.TestCase):

    def setUp(self):
        # Create a database object
        self.db_object = Dtb()
        self.db_object.create_tables()
        self.app = create_app(config_name="testing")
        # Creates a test client for this application.
        self.test_client = self.app.test_client()
        # Adming signup details
        self.admin_info = json.dumps({
            "username": "kiptoo",
            "email": "kiptoo@mail.com",
                        "password": "Kiptoo5600@",
                        "role": "admin"
        })

        self.attendant_info = json.dumps({
            "username": "hesbon",
            "email": "hesbon@gmail.com",
            "password": "Hesbon5600@",
            "role": "attendant"
        })
        # Signup admin
        self.signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_info,
                                             content_type='application/json')

        signup_attendant = self.test_client.post("/api/v2/auth/signup",
                                                 data=self.attendant_info,
                                                 headers={
                                                     'content-type': 'application/json'
                                                 })

        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        # Delete the created
        self.db_object.destroy_tables()
        return self.context.pop()
