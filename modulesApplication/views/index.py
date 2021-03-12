from django.shortcuts import render


def index(request):
    return render(request, 'modulesApplication/main/index.html')
