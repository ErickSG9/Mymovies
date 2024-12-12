from django.urls import path
from .views import *

urlpatterns = [
    path('<int:movie_id>/', movie, name='movie'),
    path('movie_review/add/<int:movie_id>/', add_review),
    path('movie_reviews/<int:movie_id>/', movie_reviews, name='movie_reviews'),
    path("search", search_movies, name="search_movies"),
    path("random", random_movies, name="random_movies"),
    path('', index)
]