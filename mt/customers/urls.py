from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('<int:id>/', views.customer_detail, name='customer_detail'),
    path('create/', views.customer_create, name='customer_create'),
    path('<int:id>/edit/', views.edit_customer, name='edit_customer'),
    path('<int:id>/delete/', views.delete_customer, name='delete_customer'),
]
