from django.urls import path

from . import views

app_name = 'modulesApplication'
urlpatterns = [
    path('', views.home, name='home'),
    path('AllModules.html', views.index, name='index'),
    path('StudentLandingPage.html', views.studentLanding, name='studentLanding'),
    path('StudentChooseModules.html', views.studentChooseModules, name='studentChooseModules'),
    path('ReadMore.html', views.readMore, name='ReadMore'),
]
