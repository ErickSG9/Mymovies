from django.shortcuts import render
from django.http import HttpResponse 
from movies.models import Movie, MovieReview
from movies.forms import MovieReviewForm
from django.core.paginator import Paginator
from django.contrib.postgres import search
import random

# Create your views here.
def index(request):
    movies = list(Movie.objects.all())
    random_movies = []
    if movies:
        random_movies= random.sample(movies,4)
    return render(request,'movies/index.html', {'movies': random_movies} )
    
def movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    review_form = MovieReviewForm()
    context = {'movie':movie, 'saludo':'Holo','review_form':review_form} 
    return render(request, 'movies/movie.html', context=context) 
    
def movie_reviews(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request,'movies/reviews.html', context={'movie':movie })
    
def add_review(request, movie_id):
    form = None
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = MovieReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            title  = form.cleaned_data['title']
            review = form.cleaned_data['review']
            movie_review = MovieReview(
                    movie=movie,
                    rating=rating,
                    title=title,
                    review=review,
                    user=request.user)
            movie_review.save()
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'listChanged'})
    else:
        form = MovieReviewForm()
        return render(request,
                  'movies/movie_review_form.html',
                  {'movie_review_form': form, 'movie':movie})
                  
                  
                  
def random_movies(request):
    movies = list(Movie.objects.all())
    random_works = []
    if movies:
        random_works = random.sample(movies, 4)
    return render(request, 'movies/movies_random.html',
                  {'movies': random_works})
                  
def search_movies(request):
    if request.method == 'GET':
        value = request.GET['search']
        movies = ft_movies(value)

        paginator = Paginator(movies, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'movies/movie_search.html',
                      {'movies': movies, 'search_value': value,
                       "page_obj": page_obj})
    else:
        return render(request, 'movies/index.html',
                      {'movies': [], 'search_value': None})


def ft_movies(value):
    vector = (
        search.SearchVector("title", weight="A")
        
    )
    query = search.SearchQuery(value, search_type="websearch")
    return (
        Movie.objects.annotate(
            search=vector,
            rank=search.SearchRank(vector, query),
        )
        .filter(search=query)
        .order_by("-rank")
    )