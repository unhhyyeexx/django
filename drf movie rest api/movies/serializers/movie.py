from rest_framework import serializers
from ..models import Movie, Actor
from .review import ReviewListSerializer

class MovieListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('title', 'overview',)


class MovieSerializer(serializers.ModelSerializer):

    class Actor(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('name',)
    actors = Actor(read_only=True, many=True)
    review_set = ReviewListSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'actors', 'review_set', 'title', 'overview', 'release_date', 'poster_path')
        read_only_fields = ('movie',)

class MovieForeign(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title',)