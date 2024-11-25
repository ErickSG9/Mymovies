from django.shortcuts import render
from django.http import HttpResponse 
from movies.models import Movie

# Create your views here.
def index (request):
    saludo = "Hola TEC"
    return HttpResponse(saludo) 
    
def movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    
    context = {'movie':movie, 'saludo':'Holo'} 
    return render(request, 'movies/movie.html', context=context) 