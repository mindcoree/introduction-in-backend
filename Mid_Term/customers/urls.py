from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerListCreateView.as_view(), name='customer-list-create'),
    path('<int:id>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('create/', views.CustomerCreateView.as_view(), name='customer-create'),
    path('<int:id>/edit/', views.CustomerEditView.as_view(), name='customer-edit'),
    path('<int:id>/delete/', views.CustomerDeleteView.as_view(), name='customer-delete'),
]