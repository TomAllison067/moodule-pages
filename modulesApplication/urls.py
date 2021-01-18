from django.urls import path

from . import views

app_name = 'modulesApplication'
urlpatterns = [
    path('', views.index, name='index'),
]
