from database.db import Database
from security.hash import HashClass
from security.auth import AuthClass
import multiprocessing
import bcrypt

class AuthRepo():
    def __init__(self, data=''):
        self.data = data
        
    def insert_user_with_timeout(self, timeout):
        user = Database()
        idUser = user.insert_data(self.data)
        user.close_connection()
        return idUser

    def register(self):
        try:
            timeout = 2

            process = multiprocessing.Process(target=self.insert_user_with_timeout, args=(timeout,))
            process.start()

            process.join(timeout=timeout)

            if process.is_alive():
                process.terminate()
                process.join()
                return '500'
            else:
                return '200'

        except Exception as e:
            return '500'  
        
    def login(self, email, password) :
        user = Database()
        user = user.find_user_by_email(email)
        
        # Password yang dimasukkan oleh pengguna
        input_password = password

        # Mengambil hash password dari dokumen user
        hashed_password = user['password']
        
        # cek 
        is_verified = HashClass.verify_password(input_password, hashed_password)
        if is_verified:
            token = AuthClass.generate_token(str(user['_id']), user['name'], user['email'], user['role'])
            return token
        else:
            return None
        