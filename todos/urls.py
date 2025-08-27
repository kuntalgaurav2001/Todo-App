from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/todos/', views.create_todo, name='create_todo'),
    path('api/todos/<int:todo_id>/', views.update_todo, name='update_todo'),
    path('api/todos/<int:todo_id>/toggle/', views.toggle_todo, name='toggle_todo'),
    path('api/todos/<int:todo_id>/delete/', views.delete_todo, name='delete_todo'),
]