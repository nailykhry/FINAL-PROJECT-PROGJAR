import json
class AnswerTaskModel:
    def __init__(self, id_task, id_user, file):
        self.id_task = id_task
        self.id_user = id_user
        self.file = file

    def to_json(self):
        return json.dumps({
            'id_task': self.id_task,
            'id_user': self.id_user,
            'file' : self.file
        })

# Membuat objek model
model = AnswerTaskModel("ewfwef", "tuga","iqebdqi.pdf")
print(model.to_json())