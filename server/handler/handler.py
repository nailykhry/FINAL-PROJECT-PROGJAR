import os
import socket
import select
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HandlerClass():
    def __init__(self, client, address, data):
        self.client = client
        self.address = address
        self.size = 1024
        self.data = data

    def run(self):
        data = self.data
        request_header = data.split('\r\n')
        request_file = request_header[0].split()[1]
        response_header = b''
        response_data = b''
        if request_file == '/' or request_file == '/index.html':
            f = open(os.path.join(
            BASE_DIR, '../public/views/index.html'), 'r', newline='')
            response_data = f.read()
            f.close()

            content_length = len(response_data)
            response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
                + str(content_length) + '\r\n\r\n'
            
            # send
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))                    
