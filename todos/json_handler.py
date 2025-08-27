import json
import os
from datetime import datetime
from django.conf import settings


class TodoJSONHandler:
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, 'data', 'todos.json')
        self._ensure_data_directory()
        self._ensure_json_file()


    def _ensure_data_directory(self):
        data_dir = os.path.dirname(self.file_path)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _ensure_json_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([],f)

    def _read_todos(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_todos(self, todos):
        with open(self.file_path, 'w') as f:
            json.dump(todos, f, indent=2, default=str)

    def get_all_todos(self):
        return self._read_todos()

    def get_todo_by_id(self, todo_id):
        todos = self._read_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                return todo
        return None

    def create_todo(self, title, description=""):
        todos = self._read_todos()
        new_todo = {
            'id': len(todos) + 1,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
        }
        todos.append(new_todo)
        self._write_todos(todos)
        return new_todo

    def update_todo(self, todo_id, title=None, description=None, completed=None):
        todos = self._read_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                if title is not None:
                    todo['title'] = title
                if description is not None:
                    todo['description'] = description
                if completed is not None:
                    todo['completed'] = completed
                todo['updated_at'] = datetime.now().isoformat()
                self._write_todos(todos)
                return todo
        return None

    def toggle_complete(self, todo_id):
        todos = self._read_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                todo['completed'] = not todo['completed']
                todo['updated_at'] = datetime.now().isoformat()
                self._write_todos(todos)
                return todo
        return None

    def delete_todo(self, todo_id):
        todos = self._read_todos()
        todos = [todo for todo in todos if todo['id'] != todo_id]
        self._write_todos(todos)
        return True