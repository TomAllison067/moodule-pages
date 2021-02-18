from django.shortcuts import render


def landing(request):
    return render(request, 'modulesApplication/OfficeLandingPage.html')