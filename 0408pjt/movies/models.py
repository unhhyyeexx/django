from django.db import models
from distutils.command.upload import upload

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=30)
    popularity = models.FloatField()
    release_date = models.DateField()
    genre = models.TextField()
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title