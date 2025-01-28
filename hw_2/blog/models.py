from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    author = models.CharField(max_length=200)


