import json
class TaskModel:
    def __init__(self, name_course, name, description, deadline, file):
        self.name_course = name_course
        self.name = name
        self.description = description
        self.deadline = deadline
        self.file = file

    def to_json(self):
        return json.dumps({
            'name_course': self.name_course,
            'name': self.name,
            'description': self.description,
            'deadline' : self.deadline,
            'file' : self.file
        })
