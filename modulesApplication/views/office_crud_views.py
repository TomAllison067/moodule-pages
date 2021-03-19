from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from modulesApplication.auth.is_staff import is_staff_or_superuser
from modulesApplication.database.models.course_leader import CourseLeader
from modulesApplication.database.models.programme import Programme


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
    template_name = 'modulesApplication/office/crud-templates/OfficeCourseLeaderListTemplate.html'

    def get_queryset(self):
        return CourseLeader.objects.all().order_by('module')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class CourseLeaderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = CourseLeader
    fields = ['module', 'person', 'term']
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericUpdateTemplate.html'

    def test_func(self):
        return is_staff_or_superuser(self.request.user)

    success_url = reverse_lazy('modulesApplication:view-course-leaders')


class CourseLeaderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = CourseLeader
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericDeleteTemplate.html'
    success_url = reverse_lazy('modulesApplication:view-course-leaders')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class CourseLeaderCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = CourseLeader
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericCreateTemplate.html'
    success_url = reverse_lazy('modulesApplication:view-course-leaders')
    fields = ['module', 'person', 'term', 'leader']

    def test_func(self):
        return is_staff_or_superuser(self.request.user)