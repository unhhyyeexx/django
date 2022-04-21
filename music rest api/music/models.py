from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{ self.name }'


class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    
