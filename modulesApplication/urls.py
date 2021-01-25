from django.urls import path

from . import views

app_name = 'modulesApplication'
urlpatterns = [
    path('', views.home, name='home'),
    path('AllModules.html', views.index, name='index'),
]
