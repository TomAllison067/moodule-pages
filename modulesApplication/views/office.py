from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..programmeInfo import csv_converter
from ..models import Module, Programme, ModuleSelection
from ..database.csvForm import CsvUploadForm
from modulesApplication.database.csv_reader import CsvReader


def landing(request):
    return render(request, 'modulesApplication/OfficeLandingPage.html')


def csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.process_data(request.FILES['data_file'], request.POST['model'])
            print(request.POST['model'])
            # print(UploadedFile(request.FILES['data_file']).name)
            return HttpResponseRedirect('/success/url/')
    else:
        form = CsvUploadForm()
    return render(request, 'modulesApplication/OfficeCsvDownloads.html', {'form': form})


def csv_file(request, model_class):
    models = [Module, Programme, ModuleSelection]
    for model in models:
        if model.__name__ == model_class:
            model_class = model
            break
    return csv_converter.model_to_csv(model_class)
