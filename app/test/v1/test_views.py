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
            "price": 20.00,
            "quantity": 2
        })
        self.sale = json.dumps({
            "product_id": 1
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
        # print(self.create_product.data)
        self.create_sale = self.test_client.post("/api/v1/sales",
                                                 data=json.dumps({
                                                     "product_id": 1
                                                 }),
                                                 headers={
                                                     'content-type': 'application/json',
                                                     'x-access-token': self.attendant_token['token']
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
        #  Provide admin login detail
        self.admin_login_details = json.dumps({
            "username": "kiptoo",
            "email": "kiptoo@gmail.com"
        })
        response = self.test_client.post("/api/v1/auth/login",
                                         data=admin_login_details,
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

    def test_existing_username(self):
        user = json.dumps({
            "username": "hesbon",
                        "password": "slGG23@bha",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Username 'hesbon' already taken")
        self.assertEqual(response.status_code, 406)

    def test_missing_username(self):
        user = json.dumps({
            "username": "",
                        "password": "slGG23@bha",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Username is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        user = json.dumps({
            "username": "jdhgfjg",
                        "password": "",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password is missing")
        self.assertEqual(response.status_code, 400)

    def test_missing_role(self):
        user = json.dumps({
            "username": "lskfkk",
                        "password": "slGG23@bha",
                        "role": ""})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Role is missing")
        self.assertEqual(response.status_code, 400)

    def test_invalid_role(self):
        user = json.dumps({
            "username": "",
                        "password": "slGG23@bha",
                        "role": "mister"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_username_not_string(self):
        user = json.dumps({
            "username": 580,
            "password": "slGG23@bha",
                        "role": "mister"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Username must be a string")
        self.assertEqual(response.status_code, 400)

    def test_password_not_string(self):
        user = json.dumps({
            "username": "ljh6",
            "password": 85924,
            "role": "mister"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must be a string")
        self.assertEqual(response.status_code, 400)

    def test_role_not_string(self):
        user = json.dumps({
            "username": "ljh6",
            "password": "slGG23@bha",
            "role": 8925})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Role must be a string")
        self.assertEqual(response.status_code, 400)

    def test_password_less_than_6_ch(self):
        user = json.dumps({
            "username": "kipt47oo",
                        "password": "sJ2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_digit(self):
        user = json.dumps({
            "username": "kipt4afoo",
                        "password":  "sJ@#vbmJ@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must have a digit")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_uppercase(self):
        user = json.dumps({
            "username": "kipt47oo",
                        "password": "shjhg@323@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must have an upper case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_lowercase(self):
        user = json.dumps({
            "username": "kipdst47oo",
                        "password": "FUYH2B@@FYT",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must have a lower case character")
        self.assertEqual(response.status_code, 400)

    def test_password_with_no_special_ch(self):
        user = json.dumps({
            "username": "kipt47oo",
                        "password": "sJ2jfDF234j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must have one of the special charater [#@$]")
        self.assertEqual(response.status_code, 400)

    def test_password_more_than_12_ch(self):
        user = json.dumps({
            "username": "kiptoo45",
                        "password": "sJsbkhsbkkjdfnv2@j",
                        "role": "admin"})
        response = self.test_client.post("/api/v1/auth/signup", data=user,
                                         headers={
                                             'content-type': 'application/json'})
        self.assertEqual(json.loads(response.data)[
                         'message'], "Password must be at least 6 and at most 10 ch long")
        self.assertEqual(response.status_code, 400)

    def test_get_all_products(self):
        response = self.test_client.get('/api/v1/products', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_get_all_products_no_token(self):
        response = self.test_client.get('/api/v1/products')
        self.assertEqual(response.status_code, 401)

    def test_existing_product(self):
        response = self.test_client.post("/api/v1/products",
                                         data=self.product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(json.loads(response.data)[
                         'message'], "Product: 'omo' already exists")
        self.assertEqual(response.status_code, 406)

    def test_title_not_string(self):
        product = json.dumps({
            "title": 520,
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(json.loads(response.data)[
                         'message'], "Product title must be a string")
        self.assertEqual(response.status_code, 400)

    def test_description_not_string(self):
        product = json.dumps({
            "title": "Kiwi",
            "category": "toilateries",
            "description": 78768,
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_category_not_string(self):
        product = json.dumps({
            "title": "520",
            "category": 65654,
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_quantity_not_int(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": "500"
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_price_not_float(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_inventory_not_int(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 45.00,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_quantity_less_than_zero(self):
        product = json.dumps({
            "title": "dhc",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": -2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_inventory_less_than_zero(self):
        product = json.dumps({
            "title": "520",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": -1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_price_less_than_zero(self):
        product = json.dumps({
            "title": "hghgvh",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": -20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']
                                         })
        self.assertEqual(response.status_code, 400)

    def test_admin_get_all_sales(self):
        response = self.test_client.get('/api/v1/sales', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_all_sales(self):
        response = self.test_client.get('/api/v1/sales', headers={
            'x-access-token': self.attendant_token['token']})
        self.assertEqual(response.status_code, 403)

    def test_admin_get_single_sale(self):
        response = self.test_client.get('/api/v1/sales/1', headers={
            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)

    def test_attendant_get_single_sale(self):
        response = self.test_client.get('/api/v1/sales/1')
        self.assertEqual(response.status_code, 401)

    def test_get_sales(self):
        response = self.test_client.get("/api/v1/sales",
                                        headers={
                                            'content-type': 'application/json',
                                            'x-access-token': self.admin_token['token']})

        self.assertEqual(response.status_code, 200)

    def test_post_sale_attendant(self):
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_id": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 201)

    def test_post_sale_admin(self):
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_id": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.admin_token['token']})

        self.assertEqual(response.status_code, 403)

    def test_product_out_of_stock(self):
        self.test_client.post("/api/v1/sales",
                              data=json.dumps({"product_id": 1}),
                              headers={
                                  'content-type': 'application/json',
                                  'x-access-token': self.attendant_token['token']})
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_id": 1}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_post_sale_non_existent_product(self):
        response = self.test_client.post("/api/v1/sales",
                                         data=json.dumps({"product_id": 2}),
                                         headers={
                                             'content-type': 'application/json',
                                             'x-access-token': self.attendant_token['token']})

        self.assertEqual(response.status_code, 404)

    def test_admin_create_product(self):
        product = json.dumps({
            "title": "Panga Soap",
            "category": "toilateries",
            "description": "description for omo",
            "lower_inventory": 1,
            "price": 20.00,
            "quantity": 2
        })
        response = self.test_client.post("/api/v1/products",
                                         data=product,
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

    def test_get_single_product(self):
        response = self.test_client.get('/api/v1/products/1',
                                        headers={
                                            'x-access-token': self.admin_token['token']})
        self.assertEqual(response.status_code, 200)
