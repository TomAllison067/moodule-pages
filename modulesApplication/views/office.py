"""
All the views relating to a member of staff using the application, and some helper methods.
"""

import datetime
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from ..auth.is_staff import is_staff_or_superuser
from modulesApplication.csv.csvForm import CsvUploadForm
from ..models import Module, Programme, ModuleSelection, People
from ..programmeInfo import csv_converter


@login_required
@user_passes_test(is_staff_or_superuser)
def landing(request):
    """Displays the office landing to the user."""
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            result = form.process_data(request.FILES['csv_upload'], request.POST['data'])
            if result:
                message = "{}\'s successfully updated".format(result)
            else:
                message = "Error, please check file and model is correct before submitting"
        else:
            message = "ERROR updating database... form invalid"
        return render(request, 'modulesApplication/office/OfficeLandingPage.html',
                      {'form': CsvUploadForm(), 'message': message})

    else:
        form = CsvUploadForm()
        message = ''
    return render(request, 'modulesApplication/office/OfficeLandingPage.html', {'form': form})


@login_required
@user_passes_test(is_staff_or_superuser)
def csv(request):
    """The csv upload/download form."""
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            result = form.process_data(request.FILES['data_file'], request.POST['data'])
            if result:
                message = "{} successfully updated".format(result)
        else:
            message = "ERROR updating database... form invalid"
        return render(request, 'modulesApplication/office/OfficeCsvDownloads.html',
                      {'form': CsvUploadForm(), 'message': message})

    else:
        form = CsvUploadForm()
    return render(request, 'modulesApplication/office/OfficeCsvDownloads.html', {'form': form})


@login_required
@user_passes_test(is_staff_or_superuser)
def csv_file(request, model_class):
    """A helper method to convert data models to CSV format"""
    models = [Module, Programme, ModuleSelection, People]
    for model in models:
        if model.__name__ == model_class:
            model_class = model
            break
    return csv_converter.model_to_csv(model_class)


@login_required
@user_passes_test(is_staff_or_superuser)
def print_student_selections(request):
    """Returns a csv of student selections."""
    return csv_converter.csv_student_selections()


# This is not a view - and needs not protecting!
def selections_extra_details(query_set):
    """A helper method to get extra information about ModuleSelection objects given a query set."""
    selections_list = list(query_set.values())
    for selection in selections_list:
        selected = ModuleSelection.objects.get(id=selection['id'])
        modules = [m.mod_code for m in selected.module_set.all()]
        selection['modules'] = modules
        try:
            selection['programme_name'] = Programme.objects.get(prog_code=selection['programme_id']).title
        except Programme.DoesNotExist:
            selection['programme_name'] = None
    return selections_list


@login_required
@user_passes_test(is_staff_or_superuser)
def selection_requests(request):
    """Displays outstanding selection requests and handles approving/denying/commenting on them."""
    if request.method == "POST":
        selection_id = request.POST.get('selection_id')
        selection = ModuleSelection.objects.get(id=selection_id)
        selection.last_modified = datetime.datetime.now()
        selection.comments = request.POST.get('comment')

        if 'Approved' in request.POST:
            selection.status = "APPROVED"
            print('APPROVED')
            ModuleSelection
        if 'Denied' in request.POST:
            selection.status = "DENIED"
            print('DENIED')
        selection.save(update_fields=['status', 'last_modified', 'comments'])

    headers = csv_converter.get_headers(ModuleSelection)
    headers.remove('last_modified')
    headers.remove('comments')
    query_set = ModuleSelection.objects.filter(status='PENDING')
    selections_list = selections_extra_details(query_set)
    context = {'headers': headers,
               'selections_list': selections_list,
               'list_of_selections': json.dumps(selections_list, cls=DjangoJSONEncoder)}
    return render(request, 'modulesApplication/office/SelectionRequests.html', context)


@login_required
@user_passes_test(is_staff_or_superuser)
def archived_selection_requests(request):
    """Displays archived selection requests and handles modifying them."""
    if request.method == "POST":
        selection_id = request.POST.get('selection_id')
        selection = ModuleSelection.objects.get(id=selection_id)
        selection.last_modified = datetime.datetime.now()
        if 'CommentUpdate' in request.POST:
            selection.comments = request.POST.get('comment')
            selection.save(update_fields=['comments', 'last_modified'])
        else:
            selection.status = request.POST.get('Modify')
            if request.POST.get('comment') != "":
                selection.comments = request.POST.get('comment')
                selection.save(update_fields=['status', 'last_modified', 'comments'])
            selection.save(update_fields=['status', 'last_modified'])

    selections_list = ModuleSelection.objects.exclude(status='PENDING')
    selections_list = selections_extra_details(selections_list)
    headers = csv_converter.get_headers(ModuleSelection)
    context = {'headers': headers,
               'selections_list': selections_list,
               'list_of_selections': json.dumps(selections_list, cls=DjangoJSONEncoder)}
    return render(request, 'modulesApplication/office/ArchivedSelectionRequests.html', context)
