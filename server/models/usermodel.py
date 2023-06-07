import json
class UserModel:
    def __init__(self, name, password, email,  role):
        self.name = name
        self.password = password
        self.email = email
        self.role = role

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'role': self.role
        })

