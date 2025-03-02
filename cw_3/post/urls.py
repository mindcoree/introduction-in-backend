from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_threads),
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/<int:id>/', views.thread_detail, name='thread_detail'),
    path('threads/<int:id>/delete/', views.thread_delete, name='thread_delete'),
    path('threads/<int:id>/edit/', views.thread_edit, name='thread_edit'),
    path('posts/<int:id>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
]

