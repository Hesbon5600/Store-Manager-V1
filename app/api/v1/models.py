users = []
products = []


class SaveUser():
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

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
    def __init__(self, title, category,
                 description, quantity, price, lower_inventory):
        self.title = title
        self.category = category
        self.description = description
        self.quantity = quantity
        self.price = price
        self.lower_inventory = lower_inventory

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


def destroy():
    products.clear()
    users.clear()

