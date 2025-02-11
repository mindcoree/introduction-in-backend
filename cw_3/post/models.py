from django.db import models

# Create your models here.
class Thread(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,related_name='posts')

    def __str__(self):
        return self.title
