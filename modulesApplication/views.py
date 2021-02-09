from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.
def index(request):
    template_name = 'modulesApplication/index.html'
    return render(request, template_name)
#
# def home(request):
#   # Temporary!
#   return HttpResponse("Welcome to the tutorial.")