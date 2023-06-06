import os
import socket
import select
import sys
from urllib.parse import unquote

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HandlerClass():
    def __init__(self, client, address, data):
        self.client = client
        self.address = address
        self.size = 1024
        self.data = data
        self.header = ''
        self.body = ''

    def run(self):
        data = self.data
        request_header = data.split('\r\n')
        request_file = request_header[0].split()[1]
        method = request_header[0].split()[0]
        response_header = b''
        response_data = b''
        
        if method == 'GET' and (request_file == '/' or request_file == '/index.html'):
            self.index()
        
        elif method == 'GET' and (request_file == '/login'):
            self.get_login()
            
        elif method == 'POST' and (request_file == '/login'):
            self.user_login()  
        
        elif method == 'GET' and (request_file == '/register'):
            self.get_register()  
        
        elif method == 'POST' and (request_file == '/register'):
            self.user_register()  
        
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
        
    def get_login(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/login.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))  
        
    def user_login(self):
        data = self.data
        request_header = data.split('\r\n\r\n')[0]
        body = unquote(data.split('\r\n\r\n')[1])
        self.get_dashboard()
        
    
    def get_register(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/register.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8')) 
        
    def user_register(self):
        data = self.data
        request_header = data.split('\r\n\r\n')[0]
        body = unquote(data.split('\r\n\r\n')[1])
        self.redirect_to_page('/login')
        
    def get_dashboard(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/dashboard.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
