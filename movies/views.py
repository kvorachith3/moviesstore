from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
from .models import Movie, Review, HiddenMovie

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    if request.user.is_authenticated:
        movies = movies.exclude(hiddenmovie__user=request.user)

    template_data = {
        'title': 'Movies',
        'movies': movies,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
    }
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review(
            comment=request.POST['comment'],
            movie=movie,
            user=request.user
        )
        review.save()
        return redirect('movies.show', id=id)
    return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review,
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

class HiddenMoviesView(ListView):
    template_name = "movies/hidden_movies.html"
    context_object_name = "movies"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Movie.objects.none()
        return Movie.objects.filter(hiddenmovie__user=user).select_related()

@login_required
def hide_movie(request, pk):
    if request.method == "POST":
        movie = get_object_or_404(Movie, pk=pk)
        HiddenMovie.objects.get_or_create(user=request.user, movie=movie)
        messages.success(request, f"Hidden “{movie}”.")
    return redirect(request.META.get("HTTP_REFERER") or reverse("hidden_movies"))

@login_required
def unhide_movie(request, pk):
    if request.method == "POST":
        movie = get_object_or_404(Movie, pk=pk)
        HiddenMovie.objects.filter(user=request.user, movie=movie).delete()
        messages.success(request, f"Un-hidden “{movie}”.")
    return redirect(request.META.get("HTTP_REFERER") or reverse("hidden_movies"))
