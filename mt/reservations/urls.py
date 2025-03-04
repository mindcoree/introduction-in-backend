from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservation_create, name='reservation_create'),
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    path('user/<int:user_id>/', views.reservations_by_user, name='reservations_by_user'),
    path('<int:id>/update/', views.reservation_update, name='reservation_update'),
    path('<int:id>/delete/', views.reservation_delete, name='reservation_delete'),
]
