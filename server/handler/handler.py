import os
from handler.authhandler import AuthHandler
from handler.dashboard import DashboardClass
from handler.status import StatusClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HandlerClass():
    def __init__(self, client, address, data, token=''):
        self.client = client
        self.address = address
        self.size = 1024
        self.data = data
        self.header = ''
        self.body = ''
        self.token = token

    def run(self):
        data = self.data
        request_header = data.split('\r\n')
        request_file = request_header[0].split()[1]
        method = request_header[0].split()[0]
        response_header = b''
        response_data = b''
        
        if method == 'GET' and (request_file == '/' or request_file == '/index.html'):
            self.index()
        
        # AUTH
        elif method == 'GET' and (request_file == '/login'):
            auth = AuthHandler(self.client)
            auth.get_login()
            
        elif method == 'POST' and (request_file == '/login'):
            auth = AuthHandler(self.client)
            token = auth.user_login(self.data) 
            self.token = token
        
        elif method == 'GET' and (request_file == '/register'):
            auth = AuthHandler(self.client)
            auth.get_register()  
        
        elif method == 'POST' and (request_file == '/register'):
            auth = AuthHandler(self.client)
            auth.user_register(self.data)  
        # END AUTH
           
        elif method == 'GET' and (request_file == '/dashboard'):
            Auth = AuthHandler(self.client)
            token = Auth.get_bearer_code(self.data)
            
            self.token = token
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                dashboard = DashboardClass(self.client, self.token)
                dashboard.get_dashboard()
            else:
                self.redirect_to_page('/login')
            
        elif method == 'GET' and (request_file == '/500'):
            status = StatusClass(self.client)
            status.status_500()
        
        else:
            status = StatusClass(self.client)
            status.status_404()
        
    
    def redirect_to_page(self, url):
        response_header = 'HTTP/1.1 302 Found\nLocation: {}\r\n\r\n'.format(url)
        response_data = ''
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
    
    def index(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/index.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))      
        
   
