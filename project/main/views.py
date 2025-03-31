
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    data = {
        'title': 'Welcome to My Website',
        'values': ['value1', 'value2', 'value3'],
    }
    return render (request, 'main/index.html')

def about(request):
    return HttpResponse("This is the about page.")