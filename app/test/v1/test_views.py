import unittest
import json
from app.api.v1.models import destroy
from app import create_app
from instance.config import app_config


class TestsForApi(unittest.TestCase):

    def setUp(self):
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

        self.attendant_login_details = json.dumps({
                        "username": "hesbon",
                        "password": "Hesbon5600@"
                        })
        self.admin_login_details = json.dumps({
                        "username": "kiptoo",
                        "password": "Kiptoo5600@"
        })
        self.product = json.dumps({
                            "title": "omo",
                            "category": "toilateries",
                            "description": "description for omo",
                            "lower_inventory": 1,
                            "price": 20,
                            "quantity": 2
                                   })

        signup_admin = self.test_client.post("/api/v1/auth/signup",
                                             data=self.admin_info,
                                             content_type='application/json')

        login_admin = self.test_client.post("/api/v1/auth/login",
                                            data=self.admin_login_details,
                                            content_type='application/json')
        self.admin_token = json.loads(login_admin.data.decode())

        signup_attendant = self.test_client.post("/api/v1/auth/signup",
                                                 data=self.attendant_info,
                                                 content_type='application/json')

        login_attendant = self.test_client.post("/api/v1/auth/login",
                                data=self.attendant_login_details,
                                content_type='application/json')
        self.attendant_token = json.loads(login_attendant.data.decode())

        self.create_product = self.test_client.post("/api/v1/products",
                                   data=self.product,
                                   headers={
                                    'content-type': 'application/json',
                                    'x-access-token': self.admin_token['token']
                                                             })

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

    def test_admin_login(self):
        response = self.test_client.post("/api/v1/auth/login",
                                         data=self.admin_login_details,
                                         headers={
                                            'content-type': 'application/json'
                                                  })
        self.assertEqual(response.status_code, 200)

    def test_attendant_login(self):
        response = self.test_client.post("/api/v1/auth/login",
                                         data=self.attendant_login_details,
                                         headers={
                                          'content-type': 'application/json'
                                                 })

        self.assertEqual(response.status_code, 200)

    def test_wrong_signup(self):
        user = json.dumps({
                           "username": "sjdh",
                           "password": "jhdjh@3",
                           "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'
                                                 })
        self.assertEqual(response.status_code, 400)

    def test_existing_username(self):
        user = json.dumps({
                        "username": "hesbon",
                        "password": "slGG23@bha",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'})
        self.assertEqual(response.status_code, 406)

    def test_password_less_than_6_ch(self):
        user = json.dumps({
                        "username": "kipt47oo",
                        "password": "sJ2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                         'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_digit(self):
            user = json.dumps({
                            "username": "kipt4afoo",
                            "password":  "sJ@#vbmJ@j",
                            "role":"admin"})
            response = self.test_client.post("/api/v1/auth/signup", data=user,
                                             headers={
                                             'content-type': 'application/json' })
            self.assertEqual(response.status_code, 400)

    def test_password_with_no_uppercase(self):
        user = json.dumps({
                        "username": "kipt47oo",
                        "password": "shjhg@323@j",
                        "role":"admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_lowercase(self):
        user = json.dumps({
                        "username": "kipdst47oo",
                        "password": "FUYHB@@FYT",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_special_ch(self):
        user = json.dumps({
                        "username": "kipt47oo",
                        "password": "sJ2jfDF234j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_password_more_than_12_ch(self):
        user = json.dumps({
                        "username": "kiptoo45",
                        "password": "sJsbkhsbkkjdfnv2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                          'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_signup_no_data(self):
        user = json.dumps({})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                         'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_admin_create_product(self):
    
        response = self.test_client.post("/api/v1/products",
                                         data=self.product,
                                         headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 201)

    def test_attendant_create_product(self):

        response = self.test_client.post("/api/v1/products",
                                         data=self.product,
                                         headers={
                                          'content-type': 'application/json',
                                          'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 401)

    def test_get_all_products(self):
        response = self.test_client.get('/api/v1/products', headers={
                    'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_get_all_products_no_token(self):
        response = self.test_client.get('/api/v1/products')
        self.assertEqual(response.status_code, 401)
    