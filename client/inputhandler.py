import getpass

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