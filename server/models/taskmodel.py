import json
class TaskModel:
    def __init__(self, task_name, description, deadline):
        self.task_name = task_name
        self.description = description
        self.deadline = deadline

    def to_json(self):
        return json.dumps({
            'task_name': self.task_name,
            'description': self.description,
            'deadline' : self.deadline,
        })
