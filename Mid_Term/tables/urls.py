from django.urls import path
from . import views

urlpatterns = [
    path('', views.TableListCreateView.as_view(), name='table-list-create'),
    path('<int:id>/', views.TableDetailView.as_view(), name='table-detail'),
    path('create/', views.TableCreateView.as_view(), name='table-create'),
    path('<int:id>/edit/', views.TableEditView.as_view(), name='table-edit'),
    path('<int:id>/delete/', views.TableDeleteView.as_view(), name='table-delete'),
]