import os
from urllib.parse import unquote
from models.materialmodel import MaterialModel
from repository.materialsrepo import MaterialsRepo

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class MaterialClass :  
    def __init__(self, client):
        self.client = client
        
    def get_material_by_courseid(self, data) :
        request_header = data.split('\r\n')
        request_file = request_header[0].split()[1]
        _id = request_file.split('/')[-1]
        materialsObj = MaterialsRepo()
        materials = materialsObj.get_all_material_by_courseid(_id)
        
        f = open(os.path.join(BASE_DIR, '../public/views/material.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        # perbarui data dengan list course sesungguhnya
        material_list = "".join(f'<li><a href="/material/{material["_id"]}">{material["name"]}</a></li>' for material in materials)
        response_data = response_data.replace('{material_list}', material_list)
        
        # kalau bukan admin nanti dihide aja
        response_data = response_data.replace('{add_material_admin}', '<a href="/addmaterial">Tambahkan Material</a>')

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        # response_header += f'Authorization: {self.token}\r\n'
        response_header += '\r\n'

        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
    def get_add_material(self):
        f = open(os.path.join(
        BASE_DIR, '../public/views/addmaterial.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
    # def post_add_material(self, data):
    #     request_header = data.split('\r\n\r\n')[0]
    #     body = unquote(data.split('\r\n\r\n')[1])
    #     # ganti + jadi spasi biasa
    #     body = body.replace('+', ' ')
        
    #     # split dulu 
    #     name = body.split('name=')[1].split('&')[0]
    #     description = body.split('description=')[1].split()[0]
        
    #     model = CourseModel(name, description)
    #     json = model.to_json()
        
    #     repo = CoursesRepo(json)
    #     err = repo.insert_course()
        
    #     if err == 200 :
    #         self.redirect_to_page('/200')
    #     elif err == 500 :
    #         self.redirect_to_page('/500')
            
    def redirect_to_page(self, url):
        response_header = 'HTTP/1.1 302 Found\nLocation: {}\r\n\r\n'.format(url)
        response_data = ''
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))