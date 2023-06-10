import socket
import os
from inputhandler import InputHandler
from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Parser:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.size = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.response = ''
        self.header = ''
        self.content = ''

    def connect(self):
        self.socket.connect((self.host, self.port))

    def create_request_header(self, method, request_file, token):
        request_header = (method + ' ' + request_file + ' HTTP/1.1\r\n' + 'Host: ' + host + '\r\n')
        if token != '' :
            request_header = (request_header + 'Authorization: ' + token + '\r\n')
     
        request_header = request_header + '\r\n'
        request_header = request_header.encode('utf-8')
        return request_header
    
    def send_request(self, request_header):
        self.socket.send(request_header)
        
    def get_header(self):
        header = b''
        while True:
            data = self.socket.recv(self.size)
            header += data
            if b'\r\n\r\n' in header:
                break
        header = header.decode('utf-8')
        return header
    
    def add_body(self, request_header, data):
        return request_header + data.encode('utf-8') 
    
    def download_file(self, filename):
        if not os.path.exists('downloads'):
            os.mkdir('downloads')
            
        filepath = os.path.join(BASE_DIR, "downloads", filename)
        
        with open(filepath, 'wb') as f:
            while True:
                data = self.socket.recv(self.size)
                if not data:
                    break
                f.write(data)
    
    def parsing_html(self, header):

        response = b''
        while True:
            received = self.socket.recv(self.size)
            if not received:
                break
            
            response += received
            
            if (b'\r\n</html>' in received) :
                break
        
        response = response.decode('utf-8')
        soup = BeautifulSoup(header + response, 'html.parser')
        return soup.get_text()
    
    def get_status_code(self, header) :
        return header.split()[1]
    
    def disconnect(self):
        self.socket.close()

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, 'client.conf'), 'r') as file:
        lines = file.readlines()

    host = lines[1][5:14]
    port = lines[0][5:9]

    # connect
    client = Parser(host, int(port))
    client.connect()
    
    method = input('Masukkan method : ')
    request_file = input('Masukkan request file : ')
    token = input('Masukkan token : ')
    
    request_header = client.create_request_header(method, request_file, token)
    
    if method == 'POST' :
        if request_file == '/login' :
            email, password = InputHandler.login()
            request_header = client.add_body(request_header, 'email={}&password={}'.format(email, password))
        elif request_file == '/register' :
            name, email, password = InputHandler.register()
            request_header = client.add_body(request_header, 'name={}&email={}&password={}'.format(name, email, password))

    client.send_request(request_header)
    header = client.get_header()
    status_code = client.get_status_code(header)
    
    if status_code == '302' :
        print(header)
    else :
        print(client.parsing_html(header))
        
    client.disconnect()
    