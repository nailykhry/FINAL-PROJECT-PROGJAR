import os
from repository.coursesrepo import CoursesRepo
from security.auth import AuthClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class DashboardClass :  
    def __init__(self, client, token='None'):
        self.client = client
        self.token = token
    
    def get_dashboard(self, method='GET'):
        
        # Ambil payload
        payload = AuthClass.decode_token(self.token)
        role = payload['role']
        
        script = f"history.pushState(null, '', '/dashboard');"
        f = open(os.path.join(BASE_DIR, '../public/views/dashboard.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        # perbarui data dengan list course sesungguhnya
        coursesObj = CoursesRepo()
        courses = coursesObj.get_all_course()
        course_list = "".join(f'''
            <div class="m-2 text-center shadow card col-2" style="border: none;" onclick="">
                <a href="course/{course["_id"]}" style="text-decoration:none">
                <div style="background-color: #84b6ff; height: 100px;"></div>
                <div class="card-body">
                <p class="card-subtitle text-muted">{course["_id"]}</p>
                <h5 class="card-title">{course["name"]}</h5>
                </div>
                </a>
            </div>
            
        ''' for course in courses)
        response_data = response_data.replace('{course_list}', course_list)
        
        # kalau bukan admin/teacher nanti di arahin 403
        if role == 'user' :
            response_data = response_data.replace('{add_course_admin}', '<a href="/403" class="mx-5 mb-3 btn" style="background-color: #6870CB; color: white; border: none;">+ Course</a>')
        else :
            response_data = response_data.replace('{add_course_admin}', '<a href="/addcourse" class="mx-5 mb-3 btn" style="background-color: #6870CB; color: white; border: none;">+ Course</a>')

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        response_header += f'Authorization: {self.token}\r\n'
        response_header += 'Set-Cookie:{}; Path=/\r\n'.format(self.token)
        response_header += '\r\n'

        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
            
    def get_help(self, method):
        f = open(os.path.join(
        BASE_DIR, '../public/views/help.html'), 'r', newline='')
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
            
    def get_profile(self, method, token):
        # Ambil payload
        payload = AuthClass.decode_token(token)
        name = payload['name']
        email = payload['email']
        
        script = f"history.pushState(null, '', '/dashboard');"
        f = open(os.path.join(BASE_DIR, '../public/views/profile.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        response_data = response_data.replace('{detail_profile}', '<h3>Nama  :  {}<br>Email  :  {}</h3>'.format(name, email))
    
        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        response_header += f'Authorization: {self.token}\r\n'
        response_header += '\r\n'

        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))