import json
class MaterialModel:
    def __init__(self, id_course, id_user, filename):
        self.id_course = id_course
        self.id_user = id_user
        self.filename = filename

    def to_json(self):
        return json.dumps({
            'id_course': self.id_course,
            'id_user': self.id_user,
            'filename': self.filename,
        })