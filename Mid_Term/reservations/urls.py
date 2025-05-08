from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReservationCreateView.as_view(), name='reservation-list-create'),
    path('<int:id>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('user/<int:user_id>/', views.UserReservationsView.as_view(), name='user-reservations'),
    path('<int:id>/edit/', views.ReservationUpdateView.as_view(), name='reservation-edit'),
    path('<int:id>/delete/', views.ReservationDeleteView.as_view(), name='reservation-delete'),
]