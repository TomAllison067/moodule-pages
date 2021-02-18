from django.shortcuts import render

from ..programmeInfo import csv_converter
from ..models import Module, Programme, ModuleSelection


def landing(request):
    return render(request, 'modulesApplication/OfficeLandingPage.html')


def csv(request):
    return render(request, 'modulesApplication/OfficeCsvDownloads.html')


def csv_file(request, model_class):
    models = [Module, Programme, ModuleSelection]
    for model in models:
        if model.__name__ == model_class:
            model_class = model
            break
    return csv_converter.model_to_csv(model_class)
