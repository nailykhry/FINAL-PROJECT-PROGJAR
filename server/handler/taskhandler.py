import os
import re
from datetime import datetime
from urllib.parse import unquote
from models.taskmodel import TaskModel
from repository.taskrepo import TasksRepo
from security.auth import AuthClass

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
class TaskClass :  
    def __init__(self, client):
        self.client = client
        self.size = 1024
        
    def get_tasks(self, token, method) :
        # Ambil payload
        payload = AuthClass.decode_token(token)
        role = payload['role']        
        
        tasksObj = TasksRepo()
        tasks = tasksObj.get_all_task()
        
        f = open(os.path.join(BASE_DIR, '../public/views/task.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        # perbarui data dengan list course sesungguhnya
        task_list = ''.join([
            f'''
            <div class="card mx-5 mb-3 shadow" style="border: none;">
                <a href="/task/{task['_id']}" style="text-decoration:none; color:#000; font-weight:400;">
                    <div class="card-body">
                        <h5 class="card-title">Task {index + 1}</h5>
                        <p class="card-text">{task['_id']} <b>  |  </b> {task['task_name']} <b>  |  </b> Due Date: {task['deadline']}</p>
                    </div>
                </a>
            </div>
            '''
            for index, task in enumerate(tasks)
        ])
        response_data = response_data.replace('{list_task}', task_list)
        
        # kalau bukan admin/teacher nanti diarahin 403
        if role == 'user' :
            response_data = response_data.replace('{add_task_admin}', '<a href="/403" class="btn col-1 mx-5 mt-3 mb-3 shadow" style="background-color: #6870CB; color: white; border: none;">+ Task</a>')
        else :
            response_data = response_data.replace('{add_task_admin}', '<a href="/addtask" class="btn col-1 mx-5 mt-3 mb-3 shadow" style="background-color: #6870CB; color: white; border: none;">+ Task</a>')

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        response_header += f'Authorization: {token}\r\n'
        response_header += '\r\n'

        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
    def get_add_task(self, method):
        f = open(os.path.join(
        BASE_DIR, '../public/views/addtask.html'), 'r', newline='')
        response_data = f.read()
        f.close()

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n\r\n'
            
        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
        
    def post_add_task(self, data):
        
        print(data)
        task_name = data.split('task_name=')[1].split('&')[0]
        description = data.split('description=')[1].split('&')[0]
        deadline = data.split('deadline=')[1].split('\r\n')[0]
        
        model = TaskModel(task_name, description, deadline)
        json = model.to_json()
        
        repo = TasksRepo(json)
        idTask = repo.insert_task()
        
        if idTask is None :
            self.redirect_to_page('/500')
        else :
            self.redirect_to_page('/task')
    
    def get_task_detail(self, data, method) :
   
        req_file = data.split('\r\n')[0].split()[1]
        task_id = req_file.split('/')[-1]
        tasksObj = TasksRepo()
        task = tasksObj.find_one_task(task_id)
        
        f = open(os.path.join(BASE_DIR, '../public/views/task-detail.html'), 'r', newline='')
        response_data = f.read()
        f.close()
        
        date_string = task['deadline']
        formatted_date = self.format_date(date_string)

        response_data = response_data.replace('{task_id}', '{}'.format(task['_id']))
        response_data = response_data.replace('{task_name}', '{}'.format(task['task_name']))
        response_data = response_data.replace('{description}', '{}'.format(task['description']))
        response_data = response_data.replace('{deadline}', '{}'.format(formatted_date))
  

        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length:' \
            + str(content_length) + '\r\n'
        response_header += '\r\n'

        # send
        if method == 'HEAD' :
            self.client.sendall(response_header.encode('utf-8'))
        else :
            self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
        
            
    def redirect_to_page(self, url):
        response_header = 'HTTP/1.1 302 Found\nLocation: {}\r\n\r\n'.format(url)
        response_data = ''
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
         
    def format_date(self, date_string):
        try:
            date = datetime.strptime(date_string, "%Y-%m-%d")
            formatted_date = date.strftime("%d %B %Y")
            return formatted_date
        except Exception as e:
            print("Error converting date:", str(e))