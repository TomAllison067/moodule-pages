import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

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


def selections_extra_details(query_set):
    selections_list = list(query_set.values())
    for selection in selections_list:
        selected = ModuleSelection.objects.get(id=selection['id'])
        modules = [m.mod_code for m in selected.module_set.all()]
        selection['modules'] = modules
        try:
            selection['student_name'] = User.objects.get(id=selection['student_id']).first_name
            selection['programme_name'] = Programme.objects.get(prog_code=selection['programme_id']).title
        except User.DoesNotExist:
            selection['student_name'] = None
        except Programme.DoesNotExist:
            selection['programme_name'] = None
    return selections_list

@login_required
def selection_requests(request):
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
def archived_selection_requests(request):
    if request.method == "POST":
        selection_id = request.POST.get('selection_id')
        selection = ModuleSelection.objects.get(id=selection_id)
        selection.last_modified = datetime.datetime.now()
        if 'CommentUpdate' in request.POST:
            selection.comments = request.POST.get('comment')
            selection.save(update_fields=['comments', 'last_modified'])
        else:
            selection.status = request.POST.get('Modify')
            if request.POST.get('comment') is not "":
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
