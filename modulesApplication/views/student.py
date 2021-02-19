from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from ..models import Module, Programme, ModuleSelection, CourseLeader, ModuleVariant
from ..programmeInfo import factory
from modulesApplication.views import auths


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
    return render(request, 'modulesApplication/AllModules.html', context=context)


def modules_by_programme(request, prog_code, entry_year='2019'):
    prog_info = factory.get_programme_info(prog_code, entry_year)
    context = {'info': prog_info}
    return render(request, 'modulesApplication/foo.html', context)


def landing(request):
    context = auths.initialize_context(request)
    return render(request, 'modulesApplication/StudentLandingPage.html', context)


def choose_modules(request):
    if request.method == "POST":
        prog_code = request.POST.get('programme')
        stage = request.POST.get('stage')
        if prog_code is None or stage is None:
            return HttpResponseRedirect(reverse("modulesApplication:choose-modules"))
        url = reverse('modulesApplication:choose-specific-modules', kwargs={'prog_code': prog_code, 'stage': stage})
        return HttpResponseRedirect(url)
    return render(request, 'modulesApplication/StudentChooseModules.html')


def choose_specific_modules(request, prog_code, stage):
    if request.method == "GET":
        try:
            info = factory.get_programme_info(prog_code, entry_year='2019')
        except Programme.DoesNotExist:
            raise Http404
        context = {'info': info,
                   'stage': "stage{}".format(stage)}
        return render(request, 'modulesApplication/DegreeChooseModules.html', context=context)


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
        mod_codes = request.POST.getlist('module-selections')
        selection, created = ModuleSelection.objects.get_or_create(student_id=student_id, stage=stage, status="PENDING")
        for m in mod_codes:
            module = Module.objects.get(mod_code=m)
            module.selections.add(selection)
        print(selection)
        print([m.title for m in selection.module_set.all()])
        print("Count:", ModuleSelection.objects.count())
        return HttpResponseRedirect(reverse("modulesApplication:submitted",
                                            kwargs={'student_id': student_id,
                                                    'stage': stage}))
    else:
        raise Http404


def submitted(request, student_id, stage):
    print(student_id)
    selection = get_object_or_404(ModuleSelection, student_id=student_id, stage=stage, status="PENDING")
    modules = selection.module_set.all()
    context = {'selection': selection,
               'modules': modules}
    return render(request, 'modulesApplication/ViewStudentSelection.html', context=context)


def module_details(request, module):
    current_module = Module.objects.get(pk=module)

    context = {'module': current_module,
               'details': {'Summary': current_module.summary,
                           'Learning_Outcomes': current_module.learning_outcomes,
                           'Recommended_Reading': current_module.core_reading,
                           'Exam_Format': current_module.exam_format}
               }
    return render(request, 'modulesApplication/ModuleDetails.html', context=context)

