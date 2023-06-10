import os
import re
import socket
import select
import sys
import threading
from handler.handler import HandlerClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
    def run(self):
        self.open_socket()
        input_list = [self.server, sys.stdin]
        running = 1
        while running:
            input_ready, _, _ = select.select(input_list, [], [])

            for s in input_ready:

                if s == self.server:
                    # handle the server socket
                    client_socket, client_address = self.server.accept()
                    c = Client(client_socket, client_address)
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    _ = sys.stdin.readline()
                    running = 0

        # close all threads
        self.server.close()
        for c in self.threads:
            c.join()


class Client(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            decoded_data = data.decode('utf-8')
            
            if decoded_data:
                handler = HandlerClass(self.client, self.address, decoded_data)
                handler.run()
            
            else:
                self.client.close()
                running = 0
            


if __name__ == '__main__':
    # TODO: Parse and set the host and port from the config file
    with open(os.path.join(BASE_DIR, 'server.conf'), 'r') as file:
        lines = file.readlines()

    host = lines[1][5:14]
    port = lines[0][5:9]

    server = HTTPServer(host, int(port))
    server.run()