from django.shortcuts import render


def index(request):
    return render(request, 'modulesApplication/index.html')
