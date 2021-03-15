import datetime
import json

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.views import generic

from modulesApplication.database.models.module_selection import ModuleSelection
from modulesApplication.models import Programme
from modulesApplication.programmeInfo import csv_converter
from modulesApplication.views import selections_extra_details


@login_required
def landing(request):
    return render(request, 'modulesApplication/academic/AcademicLandingPage.html')


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
    return render(request, 'modulesApplication/academic/SelectionRequests-AcademicView.html', context)


class ProgrammeIndexView(generic.ListView):
    model = Programme
    template_name = "modulesApplication/academic/ViewAllProgrammes.html"

    def get_queryset(self):
        return Programme.objects.all().order_by('prog_code')


class ProgrammeUpdate(generic.UpdateView):
    model = Programme
    fields = ['title', 'level']
    template_name = 'modulesApplication/academic/UpdateProgramme.html'
