import unittest
import json
from app.api.v1.models import destroy
from app import create_app
from instance.config import app_config


class TestsForApi(unittest.TestCase):

    def setUp(self):
        # destroy()
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.admin_info = json.dumps({
                        "username": "kiptoo",
                        "password": "Kiptoo5600@",
                        "role": "admin"
                        })
        self.attendant_info = json.dumps({
                        "username": "hesbon",
                        "password": "Hesbon5600@",
                        "role": "attendant"
                        })

        signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_info,
                                             content_type='application/json')

        signup_attendant = self.test_client.post("/api/v1/auth/signup",
                                                 data=self.attendant_info,
                                                 content_type='application/json')

        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        destroy()
        return self.context.pop()

    def test_admin__signup(self):
        admin_info = json.dumps({
                        "username": "heSbon52",
                        "password": "Kiptoo5600@",
                        "role": "admin"
                        })
        response = self.test_client.post("/api/v1/auth/signup",
                                         data=admin_info, 
                                         headers={
                                          'content-type': 'application/json'
                                                 })
        self.assertEqual(response.status_code, 201)

    def test_attendant__signup(self):
        attendant_info = json.dumps({
                        "username": "kiptoo2",
                        "password": "Kiptoo500@",
                        "role": "attendant"
                                     })
        response = self.test_client.post("/api/v1/auth/signup",
                                         data=attendant_info, 
                                         headers={
                                          'content-type': 'application/json'
                                                  })
        self.assertEqual(response.status_code, 201)

