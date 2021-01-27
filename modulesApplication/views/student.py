from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from ..models import Module


def index(request):
    # Redirect to landing.. is this redundant?
    return HttpResponseRedirect(reverse('modulesApplication:student-landing'))


def all_modules(request):
    modules_list = Module.objects.all()
    module_summaries = []
    for module in modules_list:
        if module.status != 'ACTIVE':
            continue
        code = module.mod_code + " - " + module.title
        summary = "<no description available>" if module.summary == "" else module.summary
        mod_sum = {"module_code": code, "summary": summary}
        module_summaries.append(mod_sum)
    context = {'module_summaries': module_summaries}
    return render(request, 'modulesApplication/AllModules.html', context=context)


def landing(request):
    return render(request, 'modulesApplication/StudentLandingPage.html')


def choose_modules(request):
    return render(request, 'modulesApplication/StudentChooseModules.html')
