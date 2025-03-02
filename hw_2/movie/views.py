from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Movie


def movies_list(request):
    """
    Возвращает список всех фильмов в формате JSON.
    """
    movies = Movie.objects.all().values('id', 'title', 'description', 'producer', 'duration')
    return JsonResponse(list(movies), safe=False)  # safe=False позволяет вернуть список


def movie_detail(request, id):
    """
    Возвращает информацию о конкретном фильме по ID в формате JSON.
    """
    movie = get_object_or_404(Movie, id=id)
    movie_data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "producer": movie.producer,
        "duration": movie.duration,
    }
    return JsonResponse(movie_data)