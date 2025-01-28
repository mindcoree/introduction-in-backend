from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movies_list, name='movies-list'),  # GET /movies/
    path('movies/<int:id>/', views.movie_detail, name='movie-detail'),  # GET /movies/:id
]

