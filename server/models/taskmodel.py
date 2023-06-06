import json
class TaskModel:
    def __init__(self, name_course, name, description, file):
        self.name_course = name_course
        self.name = name
        self.description = description
        self.file = file

    def to_json(self):
        return json.dumps({
            'name_course': self.name_course,
            'name': self.name,
            'description': self.description,
            'file' : self.file
        })

# Membuat objek model
model = TaskModel("IPA", "tugas pelajari", "silakan", "iqebdqi.pdf")
print(model.to_json())