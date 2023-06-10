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
        
        f = open(os.path.join(BASE_DIR, '../public/views/course_material.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        # perbarui data dengan list course sesungguhnya
        material_list = "".join(f'<li><a href="/material/{material["filename"]}" style="color:#6870CB">{material["filename"]}</a></li>' for material in materials)
        response_data = response_data.replace('{material_list}', material_list)
        
        # kalau bukan admin nanti dihide aja
        response_data = response_data.replace('{add_material_admin}', '<a href="/addmaterial/{}" class="m-3 btn col-1" style="background-color: #6870CB; color: white; border: none;">+ Material</a>'.format(_id))
        response_data = response_data.replace('{id_course}', '{}'.format(_id))

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
        
        
    def download_material(self, header):
        request_header = header.split('\r\n')
        request_file = request_header[0].split()[1]
        filename = unquote(request_file.split('/')[-1])
        
        filepath = os.path.join(BASE_DIR, "..", "public", "files", "materials",filename)
        
        file_extention = os.path.splitext(filepath)[-1]
        response_data = b''
        with open(filepath, 'rb') as f:
            data = f.read()
            while(data):
                response_data = bytes.join(b'', [response_data, data])
                data = f.read()
            
        content_length = len(response_data)

        response_header = b'HTTP/1.1 200 OK\nContent-Type: application/'+file_extention.encode('utf-8')+b'; charset=UTF-8\nContent-Length:' \
                        + str(content_length).encode('utf-8') + b'\r\n\r\n'

        self.client.sendall(response_header + response_data)
        
        
    def post_add_material(self, header, filename):
        # split dulu 
        referer = header.split('Referer: ')[1].split('\r\n')[0]
        id_course = referer.split('/')[-1]
        id_user = 'weiyvfgewigfiew'
 
        model = MaterialModel(id_course, id_user, filename)
        json = model.to_json()
        
        repo = MaterialsRepo(json)
        err = repo.insert_material()
        
        if err == 200 :
            self.redirect_to_page('/200')
        elif err == 500 :
            self.redirect_to_page('/500')
            
    def redirect_to_page(self, url):
        response_header = 'HTTP/1.1 302 Found\nLocation: {}\r\n\r\n'.format(url)
        response_data = ''
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))