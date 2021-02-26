from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..programmeInfo import csv_converter
from ..models import Module, Programme, ModuleSelection
from ..database.csvForm import CsvUploadForm
from modulesApplication.database.csv_reader import CsvReader


@login_required
def landing(request):
    return render(request, 'modulesApplication/OfficeLandingPage.html')


@login_required
def csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.process_data(request.FILES['data_file'], request.POST['model'])
            # print(request.POST['model'])
            message = "database successfully updated"
            return render(request, 'modulesApplication/OfficeCsvDownloads.html', {'form': CsvUploadForm(), 'message': message})
    else:
        form = CsvUploadForm()
        message  = ""
    return render(request, 'modulesApplication/OfficeCsvDownloads.html', {'form': form, 'message': message})


@login_required
def csv_file(request, model_class):
    models = [Module, Programme, ModuleSelection]
    for model in models:
        if model.__name__ == model_class:
            model_class = model
            break
    return csv_converter.model_to_csv(model_class)
