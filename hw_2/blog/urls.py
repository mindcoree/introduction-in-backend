from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.articles_list, name='articles-list'),  # GET /articles/
    path('articles/<int:id>/', views.article_detail, name='article-detail'),  # GET /articles/:id
]
