from database.db import Database
import json
class MaterialsRepo():
    def __init__(self, data=''):
        self.data = data
        
    def insert_material(self):
        material = Database(collection="materials")
        idMaterial = material.insert_data(self.data)
        material.close_connection()
        return idMaterial
    
    def get_all_material_by_courseid(self, courseid):
        materialObj = Database(collection="materials")
        materials = materialObj.find_collection_by_courseid(courseid)
        return materials

        