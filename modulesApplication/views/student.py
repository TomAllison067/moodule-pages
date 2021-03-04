from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from ..models import Module, Programme, ModuleSelection, CourseLeader, ModuleVariant
from ..programmeInfo import factory
from ..programmeInfo.selection_validator import SelectionValidator


@login_required
def all_modules(request, sort=0):
    modules_list = Module.objects.order_by('level', 'mod_code')

    if sort != 0:
        modules_list = modules_list.filter(level=sort + 3)
    module_summaries = {}  # A dict of lists of modules separated by year
    for module in modules_list:
        if module.status != 'ACTIVE':
            continue

        # Collecting Course Leader Information
        this_module = Module.objects.get(pk=module.mod_code)
        course_leaders = CourseLeader.objects.filter(module=this_module)

        people = []
        if course_leaders.count() > 0:  # If we have course leaders for this module, append their names
            for cl in course_leaders:
                people.append(cl.person.name)
        else:  # If we couldn't find any, see if this module is a variant of another
            try:
                variant_leaders = CourseLeader.objects.filter(module=ModuleVariant.objects.get(minor=this_module).major)
            except ModuleVariant.DoesNotExist:
                variant_leaders = None
            if variant_leaders:
                people = [vl.person.name for vl in variant_leaders]

        people = ["No listed course leaders"] if len(people) == 0 else people
        summary = "<no description available>" if module.summary == "" else module.summary
        mod_sum = {"module_code": module.mod_code,
                   "title": module.title,
                   "summary": summary,
                   "learning_outcomes": module.learning_outcomes,
                   "recommended_reading": module.core_reading,
                   "exam_format": module.exam_format,
                   "course_leaders": people}
        module_summaries.setdefault(module.level, []).append(mod_sum)  # Creates a list if it doesn't exist and appends
    context = {'module_summaries': module_summaries}
    return render(request, 'modulesApplication/student/AllModules.html', context=context)


@login_required
def landing(request):
    return render(request, 'modulesApplication/student/StudentLandingPage.html')


@login_required
def choose_modules(request):
    if request.method == "POST":
        prog_code = request.POST.get('programme')
        stage = request.POST.get('stage')
        entry_year = request.POST.get('entry_year') or '2019'
        if prog_code is None or stage is None:
            return HttpResponseRedirect(reverse("modulesApplication:choose-modules"))
        url = reverse('modulesApplication:choose-specific-modules',
                      kwargs={'prog_code': prog_code,
                              'stage': stage,
                              'entry_year': entry_year})
        return HttpResponseRedirect(url)
    return render(request, 'modulesApplication/student/StudentChooseModules.html')


@login_required
def choose_specific_modules(request, prog_code, stage, entry_year, prerequisites=None, banned_combination=None):
    if request.method == "GET":
        try:
            info = factory.get_programme_info(prog_code, stage=int(stage), entry_year=entry_year)
        except Programme.DoesNotExist:
            raise Http404
        try:
            modules_list = Module.objects.order_by('level', 'mod_code')
            for module in modules_list:
                prerequisites = module.prerequisites
                banned_combinations = module.banned_combinations
        except Module.DoesNotExist:
            prerequisites = None
            banned_combinations = None
        context = {'info': info,
                   'stage': "stage{}".format(stage),
                   'prerequisites': prerequisites,
                   'banned_combinations': banned_combinations
                   }
        return render(request, 'modulesApplication/student/DegreeChooseModules.html', context=context)


@login_required
def submit_selection(request):
    if request.method == "POST":
        student_id = request.POST.get('student-id')
        if student_id == "" or student_id is None:
            messages.add_message(request, messages.ERROR, "ERROR: Please enter your student id.")
            return HttpResponseRedirect(reverse("modulesApplication:choose-specific-modules",
                                                kwargs={'prog_code': request.POST.get('prog_code'),
                                                        'stage': request.POST.get('stage')}
                                                ), messages)
        stage = request.POST.get('stage')
        mod_codes = set(request.POST.getlist('module-selections'))
        print("POST form mod codes", mod_codes)
        entry_year = request.POST.get('entry_year')
        prog_code = request.POST.get('prog_code')
        programme = Programme.objects.get(pk=prog_code)
        ModuleSelection.objects.filter(
            student_id=student_id).delete()  # Delete any existing selections (should only be one!)
        selection = ModuleSelection.objects.create(
            student_id=student_id, stage=stage, entry_year=entry_year, status="PENDING", programme=programme)
        for m in mod_codes:
            module = Module.objects.get(mod_code=m)
            module.selected_in.add(selection)
        if SelectionValidator(selection).validate():
            return HttpResponseRedirect(reverse("modulesApplication:submitted",
                                                kwargs={'student_id': student_id,
                                                        'stage': stage,
                                                        'entry_year': entry_year,
                                                        'prog_code': prog_code}))
        else:
            messages.add_message(request, messages.ERROR, "ERROR: Invalid selection.")
            return HttpResponseRedirect(reverse("modulesApplication:choose-specific-modules",
                                                kwargs={'prog_code': request.POST.get('prog_code'),
                                                        'stage': request.POST.get('stage'),
                                                        'entry_year': entry_year}
                                                ), messages)
    else:
        raise Http404


@login_required
def submitted(request, student_id, stage, entry_year, prog_code):
    print(student_id)
    programme = Programme.objects.get(pk=prog_code)
    selection = get_object_or_404(
        ModuleSelection,
        student_id=student_id, stage=stage, entry_year=entry_year, status="PENDING", programme=programme)
    modules = selection.module_set.all()
    context = {'selection': selection,
               'modules': modules}
    return render(request, 'modulesApplication/student/ViewStudentSelection.html', context=context)


@login_required
def my_selection(request):
    """A view for the student to see their current ModuleSelection object."""
    selection = get_object_or_404(
        ModuleSelection,
        student_id=request.user.id
    )
    modules = selection.module_set.all()
    context = {
        'selection': selection,
        'modules': modules
    }
    return render(request, 'modulesApplication/student/ViewStudentSelection.html', context=context)


@login_required
def module_details(request, module):
    current_module = Module.objects.get(pk=module)

    context = {'module': current_module,
               'details': {'Summary': current_module.summary,
                           'Learning_Outcomes': current_module.learning_outcomes,
                           'Recommended_Reading': current_module.core_reading,
                           'Exam_Format': current_module.exam_format}
               }
    return render(request, 'modulesApplication/student/ModuleDetails.html', context=context)
