import json
class MaterialModel:
    def __init__(self, id_course, id_user, name,  file):
        self.id_course = id_course
        self.id_user = id_user
        self.name = name
        self.file = file

    def to_json(self):
        return json.dumps({
            'id_course': self.id_course,
            'id_user': self.id_user,
            'name': self.name,
            'file': self.file
        })