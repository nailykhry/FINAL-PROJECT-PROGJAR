import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class StatusClass :  
    def __init__(self, client):
        self.client = client
        
    def status_200(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/status/200.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))    
    
        
    def status_500(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/status/500.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 500 Internal Server Error\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
    def status_404(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/status/404.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 404 Not Found\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))