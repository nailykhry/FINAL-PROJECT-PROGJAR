import jwt

SECRET_KEY = 'secret_key'

class AuthClass:
    @staticmethod
    def generate_token(id, name, email, role):
        payload = {'id': id, 'name': name, 'email': email, 'role': role}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.InvalidTokenError:
            return None

    # @staticmethod
    # def login(username, password):
    #     if username == 'john' and password == 'secret':
    #         token = AuthClass.generate_token(username)
    #         return token

    #     return None

    @staticmethod
    def protected(token):
        payload = AuthClass.decode_token(token)

        if payload:
            return f"Welcome, {payload['username']}! This is a protected route."

        return "Invalid token."
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return True
        except jwt.InvalidTokenError:
            return False
        


# # Login dan dapatkan token
# token = AuthClass.login('john', 'secret')
# if token:
#     print("Token:", token)
# else:
#     print("Invalid username or password.")

# # Gunakan token untuk mengakses rute yang dilindungi
# response = AuthClass.protected(token)
# print(response)
