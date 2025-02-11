from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.todo_list, name='todo_list'),
    path('todos/<int:id>/', views.todo_detail, name='todo_detail'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:id>/delete/', views.todo_delete, name='todo_delete'),
]