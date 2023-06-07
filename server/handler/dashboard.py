import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class DashboardClass :  
    def __init__(self, client, token='None'):
        self.client = client
        self.token = token
        
    def get_dashboard(self):
        script = f"history.pushState(null, '', '/dashboard');"
        response_data = f"<script>{script}</script>"
        f = open(os.path.join(
        BASE_DIR, '../public/views/dashboard.html'), 'r', newline='')
        response_data += f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        response_header += f'Authorization: {self.token}\r\n'
        response_header += '\r\n'

            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))