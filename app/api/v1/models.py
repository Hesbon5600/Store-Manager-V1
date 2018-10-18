users = []


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

def destroy():
    users.clear()
