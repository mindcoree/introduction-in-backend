# posts/models.py
from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    picture = models.FileField(upload_to='posts_pictures/', blank=True, null=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
