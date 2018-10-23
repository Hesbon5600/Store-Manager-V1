from werkzeug.security import generate_password_hash, check_password_hash

users = []
products = []
sales = []


class SaveUser():
    def __init__(self, data):
        self.username = data['username']
        self.password = generate_password_hash(data['password'], method='sha256')
        self.role = data['role']

    def save_user(self):
        id = len(users) + 1
        user = {
            'id': id,
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
        users.append(user)


class PostProduct():
    def __init__(self, data):
        self.title = data['title']
        self.category = data['category']
        self.description = data['description']
        self.quantity = data['quantity']
        self.price = data['price']
        self.lower_inventory = data['lower_inventory']

    def save_product(self):
        id = len(products) + 1
        item = {
            'id': id,
            'title': self.title,
            'description': self.description,
            'quantity': self.quantity,
            'category': self.category,
            'price': self.price,
            'lower_inventory': self.lower_inventory
            }
        products.append(item)


class SaveSale():
    def __init__(self, sale):
        self.sale = sale

    def save_sale(self):
        sales.append(self.sale)


def destroy():
    products.clear()
    users.clear()
    sales.clear()
