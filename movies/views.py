from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from .models import Movie
from .forms import MovieForm
import requests

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
if not Movie.objects.all():
    for movie in data['results'][:6]:
        genre_ids = movie["genre_ids"]
        genre_name = ''
        for i in genres['genres']:
            if i["id"] == genre_ids[0]:
                genre_name += i["name"]
        
        title = movie["title"]
        popularity = movie["popularity"]
        release_date = movie["release_date"]
        genre = genre_name
        score = movie["vote_average"]
        poster_url = img_url + movie["poster_path"]
        description = movie["overview"]
        
    
        movie = Movie()
        movie.title = title
        movie.popularity = popularity
        movie.release_date = release_date
        movie.genre = genre
        movie.score = score
        movie.poster_url = poster_url
        movie.description = description
        movie.save()



@require_safe
def index(request):
    movies = Movie.objects.order_by('-pk')
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    if request.POST:
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form' : form,
    }
    return render(request, 'movies/create.html', context)

@require_safe
def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie' : movie,
        'form' : form,
    }
    return render(request, 'movies/update.html', context)