from flask import Blueprint
from flask_restful import Api
from .views import Product, Sale, SingleProduct, SingleSale
from .views import UserRegistration, UserLogin
v1 = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(v1)

api.add_resource(Product, '/products')
api.add_resource(SingleProduct, '/products/<productID>')
api.add_resource(Sale, '/sales')
api.add_resource(SingleSale, '/sales/<saleID>')
api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')
