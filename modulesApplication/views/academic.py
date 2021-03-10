from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def landing(request):
    return render(request, 'modulesApplication/academic/AcademicLandingPage.html')