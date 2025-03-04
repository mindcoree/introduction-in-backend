from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('<int:id>/', views.reservation_detail, name='reservation_detail'),
    path('create/', views.reservation_create, name='reservation_create'),
    path('<int:id>/delete/', views.reservation_delete, name='reservation_delete'),
    path('user/<int:user_id>/', views.reservations_by_user, name='reservations_by_user'),
]
