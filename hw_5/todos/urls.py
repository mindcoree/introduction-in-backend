from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.login_view,name = 'login'),
    path('logout/',views.logout_view,name = 'logout'),

    path('todos/',views.todo_list,name = 'todo_list'),
    path('todos/<int:id>/',views.todo_detail,name = 'todo_detail'),
    path('todos/add/',views.todo_add,name = 'todo_add'),
    path('todos/<int:id>/delete/',views.todo_delete,name = 'todo_delete'),
]
