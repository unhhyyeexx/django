
from rest_framework import serializers
from .movie import MovieForeign, MovieSerializer
from ..models import Actor

class ActorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    movies = MovieForeign(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ('id', 'movies', 'name',)

