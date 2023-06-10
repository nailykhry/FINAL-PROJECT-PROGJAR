from pymongo import MongoClient
import json

class Database:
    def __init__(self, host='localhost', port=27017, database='edu-airy', collection='users'):
        self.client = MongoClient(f'mongodb://{host}:{port}')
        self.db = self.client[database]
        self.collection = self.db[collection]

    def insert_data(self, data):
        data_dict = json.loads(data)
        result = self.collection.insert_one(data_dict)
        return result.inserted_id
    
    def find_user_by_email(self, email):
        query = {'email': email}
        user = self.collection.find_one(query)
        return user
    
    def get_all(self):
        collections = self.collection.find()
        return collections
    
    def find_collection_by_courseid(self, id):
        query = {'id_course': id}
        collections = self.collection.find(query)
        return collections

    def close_connection(self):
        self.client.close()


# # Membuat instance kelas UserDatabase
# user_db = UserDatabase()

# # Data yang ingin dimasukkan ke koleksi "users"
# data = {'nama': 'naily aja'}

# # Memasukkan data ke koleksi "users"
# # inserted_id = user_db.insert_user(data)
# # print("Data berhasil dimasukkan. ID:", inserted_id)

# user = user_db.find_user_by_email("nailykhairiya@gmail.com")
# print(user)

# # Menutup koneksi ke MongoDB
# user_db.close_connection()
