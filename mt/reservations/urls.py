from django.urls import path
from . import views

urlpatterns = [
    # Детали брони и обновление статуса через один URL:
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    # Удаление брони (здесь используется POST для удаления):
    path('<int:id>/delete/', views.reservation_delete, name='reservation_delete'),
    # Список броней для конкретного пользователя:
    path('user/<int:user_id>/', views.reservations_by_user, name='reservations_by_user'),
]
