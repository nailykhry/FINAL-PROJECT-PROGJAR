from database.db import Database
import json
class MaterialsRepo():
    def __init__(self, data=''):
        self.data = data
        
    def insert_task(self):
        task = Database(collection="tasks")
        idTask = task.insert_data(self.data)
        task.close_connection()
        return idTask
    
    def get_all_task(self):
        taskObj = Database(collection="tasks")
        tasks = taskObj.get_all()
        return tasks

        