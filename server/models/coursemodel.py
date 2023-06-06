import json
class CourseModel:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
        })

# Membuat objek model
model = CourseModel("IPA", "mempelajari ilmu alam")
print(model.to_json())