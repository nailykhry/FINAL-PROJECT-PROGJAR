import json
class MaterialModel:
    def __init__(self, name_course, name_user, name, description,  file):
        self.name_course = name_course
        self.name_user = name_user
        self.name = name
        self.description = description
        self.file = file

    def to_json(self):
        return json.dumps({
            'name_course': self.name_course,
            'name_user': self.name_user,
            'name': self.name,
            'descriptions': self.description,
            'file': self.file
        })

# Membuat objek model
model = MaterialModel("ipa", "naily", "kenapa bumi bulat", "menjelaskan soal bumi", "eifbiewq.pdf")
print(model.to_json())