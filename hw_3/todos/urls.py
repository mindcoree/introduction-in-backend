from django.urls import path
from .views import TodoListView, TodoDetailView, create_todo, TodoDeleteView

urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('<int:pk>/', TodoDetailView.as_view(), name='todo-detail'),
    path('new/', create_todo, name='todo-create'),
    path('<int:pk>/delete/', TodoDeleteView.as_view(), name='todo-delete'),
]