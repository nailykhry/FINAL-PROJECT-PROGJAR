from database.db import Database
import json
from bson.objectid import ObjectId

class TasksRepo():
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
    
    def find_one_task(self, string_id) :
        taskObj = Database(collection="tasks")
        object_id = self.convert_to_objectid(string_id)
        task = taskObj.find_one_by_id(object_id)
        
        if task:
            return task
        else:
            return None

    
    def convert_to_objectid(self, string_id):
        try:
            object_id = ObjectId(string_id)
            return object_id
        except Exception as e:
            print("Error converting to ObjectId:", str(e))