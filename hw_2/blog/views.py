
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Article

def articles_list(request):
    """
    Возвращает список всех статей в формате JSON.
    """
    articles = Article.objects.all().values('id', 'title', 'text', 'author')
    return JsonResponse(list(articles), safe=False)  # safe=False позволяет вернуть список


def article_detail(request, id):
    """
    Возвращает информацию о конкретной статье по ID в формате JSON.
    """
    article = get_object_or_404(Article, id=id)
    article_data = {
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "author": article.author,
    }
    return JsonResponse(article_data)
