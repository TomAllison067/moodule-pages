from django.shortcuts import render
from modulesApplication.views import *


# Create your views here.
def index(request):
    # template_name = 'modulesApplication/index.html'
    # return render(request, template_name)
    context = initialize_context(request)
    return render(request, 'modulesApplication/index.html', context)
