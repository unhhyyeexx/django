from django.shortcuts import redirect, render, get_object_or_404
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_safe
def index(request) :
    movies = Movie.objects.order_by('-pk')
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/index.html',context)

@login_required
@require_http_methods(['GET','POST'])
def create(request) :
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:detail', movie.pk)
    else :
        form = MovieForm()
    context = {
        'form' : form,
    }
    return render(request, 'movies/create.html',context)


@require_safe
def detail(request,pk):
    movie = get_object_or_404(Movie, pk=pk)
    comment_form = CommentForm()

    comments = movie.comment_set.all()
    context = {
        'movie' : movie,
        'comments' : comments,
        'comment_form' : comment_form,
    }
    return render(request, 'movies/detail.html', context)


@login_required
@require_http_methods(['GET','POST'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user == movie.user:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                movie = form.save()
                return redirect('movies:detail', movie.pk)
        else :
            form = MovieForm(instance=movie)
    else :
        return redirect('movies:index')
    context={
        'form':form,
        'movie':movie,
    }
    return render(request, 'movies/update.html', context)


@require_POST
def delete(request, pk):
    if request.user.is_authenticated :
        movie = get_object_or_404(Movie,pk=pk)
        if movie.user == request.user :
            movie.delete()
    return redirect('movies:index')


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated :
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')

@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated :
        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.user == request.user :
            comment.delete()
    return redirect('movies:detail', movie_pk)





