from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello! This is the recommender index page!")
