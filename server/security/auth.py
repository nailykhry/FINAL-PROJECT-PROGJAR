import jwt

SECRET_KEY = 'secret_key'

def generate_token(username):
    payload = {'username': username}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.InvalidTokenError:
        return None

def login(username, password):
    # Contoh validasi username dan password
    if username == 'john' and password == 'secret':
        token = generate_token(username)
        return token

    return None

def protected(token):
    payload = decode_token(token)

    if payload:
        return f"Welcome, {payload['username']}! This is a protected route."

    return "Invalid token."

# Contoh penggunaan

# Login dan dapatkan token
token = login('john', 'secret')
if token:
    print("Token:", token)
else:
    print("Invalid username or password.")

# Gunakan token untuk mengakses rute yang dilindungi
response = protected(token)
print(response)