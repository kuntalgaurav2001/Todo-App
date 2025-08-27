from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .json_handler import TodoJSONHandler

todo_handler = TodoJSONHandler()

def index(request):
    todos = todo_handler.get_all_todos()
    return render(request, 'todos/index.html', {'todos':todos})

@csrf_exempt
@require_http_methods(["POST"])
def create_todo(request):
    try:
        data = json.loads(request.body)
        title = data.get('title','').strip()
        description = data.get('description','').strip()

        if not title:
            return JsonResponse({'error':'Title is required'}, status=400)

        todo = todo_handler.create_todo(title, description)
        return JsonResponse(todo, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error':'Invalid JSON'}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_todo(request, todo_id):
    try:
        data = json.loads(request.body)
        title = data.get('title','').strip()
        description = data.get('description', '').strip()

        if not title:
            return JsonResponse({'error':'Title is required'}, status=400)

        todo = todo_handler.update_todo(todo_id, title, description)
        if todo:
            return JsonResponse(todo)
        return JsonResponse({'error':'todo not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid JSON'},status=400)


@csrf_exempt
@require_http_methods(["PUT"])
def toggle_todo(request, todo_id):
    todo = todo_handler.toggle_complete(todo_id)
    if todo:
        return JsonResponse(todo)
    return JsonResponse({'error':'todo not found'},status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_todo(request, todo_id):
    success = todo_handler.delete_todo(todo_id)
    if success:
        return JsonResponse({"message": 'todo deleted succesffully'})
    return JsonResponse({'error':'todo not found'}, status=404)


