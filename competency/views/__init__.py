from django.shortcuts import render
from . import api, api_task

# Create your views here.
def index(request):
    return render("index.html")
