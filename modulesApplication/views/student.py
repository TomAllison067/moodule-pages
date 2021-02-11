from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from ..models import Module, Programme
from ..programmeInfo import factory


# def index(request):
#     #return HttpResponseRedirect(reverse('modulesApplication:student-landing'))
#     template_name = 'modulesApplication/index.html'
#     return render(request, template_name)


def all_modules(request, sort=0):
    modules_list = Module.objects.order_by('level', 'mod_code')
    if sort != 0:
        modules_list = modules_list.filter(level=sort + 3)
    module_summaries = {}  # A dict of lists of modules separated by year
    for module in modules_list:
        if module.status != 'ACTIVE':
            continue
        summary = "<no description available>" if module.summary == "" else module.summary
        mod_sum = {"module_code": module.mod_code,
                   "title": module.title,
                   "summary": summary,
                   "learning_outcomes": module.learning_outcomes,
                   "recommended_reading": module.core_reading,
                   "exam_format": module.exam_format}
        module_summaries.setdefault(module.level, []).append(mod_sum)  # Creates a list if it doesn't exist and appends
    context = {'module_summaries': module_summaries}
    return render(request, 'modulesApplication/AllModules.html', context=context)


def modules_by_programme(request, prog_code, entry_year='2019'):
    prog_info = factory.get_programme_info(prog_code, entry_year)
    context = {'info': prog_info}
    return render(request, 'modulesApplication/foo.html', context=context)


def landing(request):
    return render(request, 'modulesApplication/StudentLandingPage.html')


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
    try:
        info = factory.get_programme_info(prog_code, entry_year='2019')
    except Programme.DoesNotExist:
        raise Http404
    context = {'info': info,
               'stage': "stage{}".format(stage)}
    return render(request, 'modulesApplication/DegreeChooseModules.html', context=context)


def module_details(request, module):
    current_module = Module.objects.get(pk=module)

    context = {'module': current_module,
               'details': {'Summary': current_module.summary,
                           'Learning_Outcomes': current_module.learning_outcomes,
                           'Recommended_Reading': current_module.core_reading,
                           'Exam_Format': current_module.exam_format}
               }
    return render(request, 'modulesApplication/ModuleDetails.html', context=context)

