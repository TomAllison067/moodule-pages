import datetime
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from modulesApplication.auth.is_staff import is_staff_or_superuser
from modulesApplication.database.models.module_selection import ModuleSelection
from modulesApplication.models import Programme, CourseLeader
from modulesApplication.programmeInfo import csv_converter
from modulesApplication.views import selections_extra_details


@login_required
@user_passes_test(is_staff_or_superuser)
def landing(request):
    return render(request, 'modulesApplication/academic/AcademicLandingPage.html')


@login_required
@user_passes_test(is_staff_or_superuser)
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


class ProgrammeIndexView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Programme
    template_name = "modulesApplication/academic/ViewAllProgrammes.html"

    def get_queryset(self):
        return Programme.objects.all().order_by('prog_code')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class ProgrammeUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Programme
    fields = ['title', 'level']
    template_name = 'modulesApplication/academic/UpdateProgramme.html'

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class CourseLeaderListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = CourseLeader
    paginate_by = 20
    template_name = 'modulesApplication/academic/crud-templates/AcademicCourseLeaderListTemplate.html'

    def get_queryset(self):
        return CourseLeader.objects.all().order_by('module')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class CourseLeaderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = CourseLeader
    fields = ['module', 'person', 'term']
    template_name = 'modulesApplication/academic/crud-templates/AcademicGenericUpdateTemplate.html'

    def test_func(self):
        return is_staff_or_superuser(self.request.user)

    success_url = reverse_lazy('modulesApplication:view-course-leaders')


class CourseLeaderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = CourseLeader
    template_name = 'modulesApplication/academic/crud-templates/AcademicGenericDeleteTemplate.html'
    success_url = reverse_lazy('modulesApplication:view-course-leaders')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class CourseLeaderCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = CourseLeader
    template_name = 'modulesApplication/academic/crud-templates/AcademicGenericCreateTemplate.html'
    success_url = reverse_lazy('modulesApplication:view-course-leaders')
    fields = ['module', 'person', 'term', 'leader']

    def test_func(self):
        return is_staff_or_superuser(self.request.user)
