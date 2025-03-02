from django.db import models

class Movie(models.Model):

    title = models.CharField(max_length=400)
    description = models.TextField()
    producer = models.CharField(max_length=400)
    duration = models.IntegerField()


    def __str__(self):
        return self.title
