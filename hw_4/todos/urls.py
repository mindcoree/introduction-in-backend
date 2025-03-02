from django.urls import path
from . import views

urlpatterns = [
    path("", views.redirect_to_todo_lists, name="home"),
    path("todo-lists/", views.todo_lists, name="todo_lists"),
    path("todo-lists/<int:id>/", views.todo_list_detail, name="todo_list_detail"),
    path("todo-lists/<int:id>/delete/", views.todo_list_delete, name="todo_list_delete"),
    path("todo-lists/<int:id>/edit/", views.todo_list_edit, name="todo_list_edit"),
    path("todos/<int:id>/delete/", views.todo_delete, name="todo_delete"),
    path("todos/<int:id>/edit/", views.todo_edit, name="todo_edit"),
]
