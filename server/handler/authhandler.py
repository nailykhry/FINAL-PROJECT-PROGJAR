import os
from models.usermodel import UserModel
from repository.authrepo import AuthRepo
from security.auth import AuthClass
from security.hash import HashClass
from urllib.parse import unquote
from handler.dashboard import DashboardClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class AuthHandler :
    def __init__(self, client):
        self.client = client
        
    def get_login(self, method, warning = ''):
        f = open(os.path.join(
        BASE_DIR, '../public/views/login.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
        
        response_data = response_data.replace('{invalid_data}', warning)    
        
        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8')) 
        
    def get_register(self, method):
        f = open(os.path.join(
        BASE_DIR, '../public/views/register.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8')) 
    
    def user_register(self, data):
        request_header = data.split('\r\n\r\n')[0]
        body = unquote(data.split('\r\n\r\n')[1])
        # ganti + jadi spasi biasa
        body = body.replace('+', ' ')
        
        # split dulu 
        name = body.split('name=')[1].split('&')[0]
        email = body.split('email=')[1].split('&')[0]
        password = body.split('password=')[1].split()[0]
        hashed_password = HashClass.hash_password(password)
        
        model = UserModel(name, hashed_password, email, 'user')
        json = model.to_json()
        
        repo = AuthRepo(json)
        err = repo.register()
        
        if err == '200' :
            self.redirect_to_page('/login')
        else :
            self.redirect_to_page('/500')
        
    def user_login(self, data):
        request_header = data.split('\r\n')[0]
        body = unquote(data.split('\r\n\r\n')[1])
        email = body.split('email=')[1].split('&')[0]
        password = body.split('password=')[1].split()[0]
        hashed_password = HashClass.hash_password(password)
        
        repo = AuthRepo()
        token = repo.login(email, password)
        if token is None :
            self.get_login('GET', "Invalid data, try again!")
        else :
            dashboard = DashboardClass(self.client, token)
            dashboard.get_dashboard()
            return token
    
        
    def get_bearer_code(self, data):
       
        if 'Cookie: ' in data :
            return data.split('Cookie: ')[1].split('\r\n')[0]
        
        try:
            return data.split('Authorization: ')[1].split('\r\n')[0]
        except IndexError:
            return None
    
    def check_authentication(self, token):
        # Lakukan validasi token autentikasi 
        if token is not None and AuthClass.verify_token(token):
            return True
        else:
            return False
        
    def redirect_to_page(self, url):
        response_header = 'HTTP/1.1 302 Found\nLocation: {}\r\n\r\n'.format(url)
        response_data = ''
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
