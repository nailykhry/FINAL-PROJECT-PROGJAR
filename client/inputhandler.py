import getpass
import os 
import pickle

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class InputHandler :
    @staticmethod
    def login() :
        email = input('Masukkan email : ')
        password = getpass.getpass("Masukkan password: ")
        return email, password
    
    @staticmethod
    def register() :
        name = input('Masukkan nama : ')
        email = input('Masukkan email : ')
        password = getpass.getpass("Masukkan password: ")
        return name, email, password
    
    @staticmethod
    def course() :
        name = input('Masukkan nama course: ')
        desc = input('Masukkan deskripsi course: ')
        return name, desc
    
    @staticmethod
    def material(sock, host, token) :
        filename = input('Masukkan nama file yang ada di folder upload: ')
        id_course = input('Masukkan id_course: ')
        filepath = os.path.join(BASE_DIR, "upload", filename)
        file_data = InputHandler.send_file(filepath)
        
        # Persiapan header
        method = "POST"
        request_file = "/materials"

        # Generate custom headers
        custom_headers = {
            "Content-Length": str(len(file_data)),  
            "Content-Type": "multipart/form-data",  
            "Authorization": token,  
        }

        # Combine custom headers into a string
        header_lines = ""
        for key, value in custom_headers.items():
            header_lines += f"{key}: {value}\r\n"

        # Construct the full request header
        request_header = f"{method} {request_file} HTTP/1.1\r\n" \
                        f"Host: {host}\r\n" \
                        f"{header_lines}\r\n\r\n" \
                        f"filename={filename}\r\n" \
                        f"id_course={id_course}\r\n"
        
        sock.send_request(request_header.encode('utf-8'))
        sock.send_request(file_data)

        print("File {} berhasil diunggah ke server".format(filename))


    
    @staticmethod
    def send_file(filepath):
        print(filepath)
        with open(filepath, 'rb') as file:
            file_data = file.read()

        return file_data