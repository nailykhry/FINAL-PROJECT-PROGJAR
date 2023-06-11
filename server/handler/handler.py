import os
import re
from urllib.parse import unquote
from handler.authhandler import AuthHandler
from handler.dashboard import DashboardClass
from handler.status import StatusClass
from handler.coursehandler import CourseClass
from handler.materialhandler import MaterialClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class HandlerClass():
    def __init__(self, client, address, undecoded_data, data, token=''):
        self.client = client
        self.address = address
        self.size = 1024
        self.undecoded_data = undecoded_data
        self.data = data
        self.header = ''
        self.body = ''
        self.token = token

    def run(self):
        data = self.data
        request_header = data.split('\r\n')
        self.header = request_header
        try:
            request_file = request_header[0].split()[1]
        except IndexError:
            print(request_header)
            
        method = request_header[0].split()[0]
        response_header = b''
        response_data = b''
        
        Auth = AuthHandler(self.client)
        token = Auth.get_bearer_code(self.data)
        
        self.token = token
        print(token)
        
        if (method == 'GET' or method == 'HEAD') and (request_file == '/' or request_file == '/index.html'):
            self.index()
        
        # MOVED PERMANENTLY
        if (method == 'GET' or method == 'HEAD') and (request_file == '/index.php'):
            response_header = 'HTTP/1.1 301 Moved Permanently\nLocation: /index.html\r\n\r\n'
            response_data = ''
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
        # AUTH
        elif (method == 'GET' or method == 'HEAD') and request_file == '/login':
            if token is None :
                auth = AuthHandler(self.client)
                auth.get_login(method)
            else:
                if Auth.check_authentication(token):
                    self.redirect_to_page('/dashboard') 
                else:
                    self.redirect_to_page('/login')
            
        elif method == 'POST' and request_file == '/login':
            auth = AuthHandler(self.client)
            token = auth.user_login(self.data) 
            self.token = token
        
        elif (method == 'GET' or method == 'HEAD') and request_file == '/register':
            if token is None :
                auth = AuthHandler(self.client)
                auth.get_register(method)
            else:
                if Auth.check_authentication(token):
                    self.redirect_to_page('/dashboard') 
                else:
                    self.redirect_to_page('/login')  
        
        elif method == 'POST' and request_file == '/register':
            auth = AuthHandler(self.client)
            auth.user_register(self.data)
              
        # END AUTH
           
        # DASHBOARD
        elif (method == 'GET' or method == 'HEAD') and request_file == '/dashboard':
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                dashboard = DashboardClass(self.client, self.token)
                dashboard.get_dashboard(method)
            else:
                self.redirect_to_page('/login')
                
        elif (method == 'GET' or method == 'HEAD') and request_file == '/help':
            help_view = DashboardClass(self.client)
            help_view.get_help(method)
            
        elif (method == 'GET' or method == 'HEAD') and request_file == '/profile':
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                profile = DashboardClass(self.client)
                profile.get_profile(method, token)
                
            else:
                self.redirect_to_page('/login')
            
        # END DASHBOARD
        
        #COURSE
        elif (method == 'GET' or method == 'HEAD') and request_file == '/addcourse' :
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                course = CourseClass(self.client)
                course.get_add_course(method)
            else:
                self.redirect_to_page('/login')
            
        elif method == 'POST' and request_file == '/course' :
            # rcv = self.client.recv(1024)
            # self.data += rcv.decode('utf-8')
            
            course = CourseClass(self.client)
            course.post_add_course(self.data)
            
        elif method == 'POST' and request_file == '/courses' :
            course = CourseClass(self.client)
            course.post_add_course(self.data)
          
        
        #END COURSE
        
        
        # MATERIAL
        elif (method == 'GET' or method == 'HEAD') and request_file.startswith('/course/'):
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                materials = MaterialClass(self.client)
                materials = materials.get_material_by_courseid(self.data, token, method)
            else:
                self.redirect_to_page('/login')
        
        elif (method == 'GET' or method == 'HEAD') and request_file.startswith('/addmaterial/'):
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                materials = MaterialClass(self.client)
                materials = materials.get_add_material(method)
            else:
                self.redirect_to_page('/login')
        
        elif (method == 'GET' or method == 'HEAD') and request_file.startswith('/material/'):
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                materials = MaterialClass(self.client)
                materials = materials.download_material(self.data, method)
            else:
                self.redirect_to_page('/login')
        
        elif (method == 'POST') and request_file == '/material':
            received_data = b""
            file_value = ''
    
            filename_match = re.search(r'filename=([^&\r\n]+)', data)
            if filename_match:
                file_value = unquote(filename_match.group(1))
                flag = False
            else:
                flag = True
            
            
            while True:
                ndata = self.client.recv(self.size)
                if flag ==  True :
                    print(ndata)
                    file_match = re.search(rb'filename="([^"]+)"', ndata)
                    if file_match:
                        file_value = file_match.group(1).decode('utf-8')
                    else:
                        file_value = None
   
                    flag = False    
                received_data += ndata
                if not ndata or (b'--\r\n' in ndata) :
                    break
            
            print("fileeeeeeeeeee", file_value)
            filepath = os.path.join(BASE_DIR, "..", "public", "files", "materials", file_value)
            with open(filepath, 'wb') as file:
                file.write(received_data)
            
            materials = MaterialClass(self.client)
            materials = materials.post_add_material(self.data, file_value)
                    
            self.redirect_to_page('/200')
          
        elif (method == 'POST') and request_file == '/materials':
            if token is None :
                self.redirect_to_page('/login')
            
            if Auth.check_authentication(token):
                materials = MaterialClass(self.client)
                materials = materials.handle_cli(self.data, self.undecoded_data)
            else:
                self.redirect_to_page('/login')
        
        # END MATERIAL    
        
        #STATUS
        elif (method == 'GET' or method == 'HEAD') and request_file == '/200' :
            status = StatusClass(self.client)
            status.status_200(method)
        
        elif (method == 'GET' or method == 'HEAD') and request_file == '/403' :
            status = StatusClass(self.client)
            status.status_403(method)
        
        elif (method == 'GET' or method == 'HEAD') and request_file == '/500' :
            status = StatusClass(self.client)
            status.status_500(method)
        
        else:
            status = StatusClass(self.client)
            status.status_404(method)
        
    
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
        method = self.header[0].split()[0]
        
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
              
        
   
