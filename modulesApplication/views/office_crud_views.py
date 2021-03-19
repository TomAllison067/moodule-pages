from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from modulesApplication.auth.is_staff import is_staff_or_superuser
from modulesApplication.models import CourseLeader, Programme, Module


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


# ====================================================================================
# Course Leaders
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


# ====================================================================================

# ====================================================================================
# Modules
class ModuleListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Module
    paginate_by = 20
    template_name = 'modulesApplication/office/crud-templates/OfficeModuleListTemplate.html'

    def get_queryset(self):
        return Module.objects.all().order_by('mod_code')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class ModuleCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Module
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericCreateTemplate.html'
    success_url = reverse_lazy('modulesApplication:staff-view-modules')
    fields = ['mod_code', 'jacs_code', 'hecos_code', 'title', 'short_title', 'level', 'department',
              'with_effect_from', 'availability_terms', 'credits', 'corequisites', 'prerequisites',
              'banned_combinations', 'learning_outcomes', 'summary', 'notional_learning_hours',
              'books_to_purchase', 'core_reading', 'exam_format', 'status', 'project', 'lab_hours',
              'deg_progs']

    def test_func(self):
        return is_staff_or_superuser(self.request.user)


class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Module
    fields = ['mod_code', 'jacs_code', 'hecos_code', 'title', 'short_title', 'level', 'department',
              'with_effect_from', 'availability_terms', 'credits', 'corequisites', 'prerequisites',
              'banned_combinations', 'learning_outcomes', 'summary', 'notional_learning_hours',
              'books_to_purchase', 'core_reading', 'exam_format', 'status', 'project', 'lab_hours',
              'deg_progs']
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericUpdateTemplate.html'

    def test_func(self):
        return is_staff_or_superuser(self.request.user)

    success_url = reverse_lazy('modulesApplication:staff-view-modules')


class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Module
    template_name = 'modulesApplication/office/crud-templates/OfficeGenericDeleteTemplate.html'
    success_url = reverse_lazy('modulesApplication:staff-view-modules')

    def test_func(self):
        return is_staff_or_superuser(self.request.user)
