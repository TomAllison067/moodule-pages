from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models import Module


def index(request):
    # Redirect to landing.. is this redundant?
    return HttpResponseRedirect(reverse('modulesApplication:student-landing'))


def all_modules(request, sort=0):
    modules_list = Module.objects.order_by('level', 'mod_code')
    if sort != 0:
        modules_list = modules_list.filter(level=sort+3)
    module_summaries = {}  # A dict of lists of modules separated by year
    for module in modules_list:
        if module.status != 'ACTIVE':
            continue
        code = module.mod_code + " - " + module.title
        summary = "<no description available>" if module.summary == "" else module.summary
        mod_sum = {"module_code": code, "summary": summary}
        module_summaries.setdefault(module.level, []).append(mod_sum)  # Creates a list if it doesn't exist and appends
    context = {'module_summaries': module_summaries}
    return render(request, 'modulesApplication/AllModules.html', context=context)


def landing(request):
    return render(request, 'modulesApplication/StudentLandingPage.html')


def choose_modules(request):
    return render(request, 'modulesApplication/StudentChooseModules.html')
