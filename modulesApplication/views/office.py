from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..programmeInfo import csv_converter
from ..models import Module, Programme, ModuleSelection, People
from ..database.csvForm import CsvUploadForm

@login_required
def landing(request):
    return render(request, 'modulesApplication/office/OfficeLandingPage.html')


@login_required
def csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            form.process_data(request.FILES['data_file'], request.POST['model'])
            # print(request.POST['model'])
            message = "database successfully updated"
        else:
            message = "ERROR updating database"
        return render(request, 'modulesApplication/office/OfficeCsvDownloads.html',
                      {'form': CsvUploadForm(), 'message': message})

    else:
        form = CsvUploadForm()
    return render(request, 'modulesApplication/office/OfficeCsvDownloads.html', {'form': form})


@login_required
def csv_file(request, model_class):
    models = [Module, Programme, ModuleSelection, People]
    for model in models:
        if model.__name__ == model_class:
            model_class = model
            break
    return csv_converter.model_to_csv(model_class)


@login_required()
def print_student_selections(request):
    return csv_converter.csv_student_selections()
