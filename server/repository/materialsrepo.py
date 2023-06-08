from database.db import Database

class MaterialsRepo():
    def __init__(self, data=''):
        self.data = data
        
    def insert_material(self):
        material = Database(collection="materials")
        idMaterial = material.insert_data(self.data)
        material.close_connection()
        return idMaterial
    
    def get_all_material(self):
        materialObj = Database(collection="materials")
        materials = materialObj.get_all()
        materialObj.close_connection()
        return materials
    
        