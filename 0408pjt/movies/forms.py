from random import choices
from turtle import textinput
from django import forms
from .models import Movie
import requests


genrelist = ['--선택--']
#api
BASE_URL = 'https://api.themoviedb.org/3'
path = '/movie/top_rated?'
genrepath = '/genre/movie/list?'
params = {
    'api_key': '473836c79a1fc815410e8bc162e748cd',
    'region': 'KR',
    'language': 'ko',
    'page' : 1
}
response = requests.get(BASE_URL+path, params=params)
data = response.json()
gresponse = requests.get(BASE_URL+genrepath, params=params)
genres = gresponse.json()


img_url= 'https://image.tmdb.org/t/p/w500'
for movie in data['results'][:6]:
    genre_ids = movie["genre_ids"]
    genre_name = ''
    for i in genres['genres']:
        if i["name"] not in genrelist:
            genrelist.append(i["name"])
        if i["id"] == genre_ids[0]:
            genre_name += i["name"]



class MovieForm(forms.ModelForm):
    genrechoice = []
    for i in range(len(genrelist)):
        genrechoice.append((i, genrelist[i]))

    title = forms.CharField(
        label= 'title',
        widget=forms.TextInput(
            attrs={
                'class' : 'my-title',
                'placeholder' : 'Title',
            }
        ),
    )
    popularity = forms.FloatField(
        label= 'popularity',
        widget=forms.TextInput(
            attrs={
                'class' : 'my-popularity',
                'placeholder' : 'Popularity',
            }
        ),
    )
    release_date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.SelectDateWidget)
    

    genre = forms.ChoiceField(
        choices = genrechoice,
        widget=forms.Select()
    )
    score = forms.FloatField(
        label= 'score',
        widget=forms.TextInput(
            attrs={
                'class' : 'my-score',
                'placeholder' : 'Score',
            }
        ),
    )
    poster_url = forms.CharField(
        label= 'poster_url',
        widget=forms.TextInput(
            attrs={
                'class' : 'my-poster_url',
                'placeholder' : 'Poster url',
            }
        ),
    )
    description = forms.CharField(
        label= 'description',
        widget=forms.TextInput(
            attrs={
                'class' : 'my-descriptionl',
                'placeholder' : 'Description',
            }
        ),
    )

    class Meta:
        model = Movie
        fields = '__all__'