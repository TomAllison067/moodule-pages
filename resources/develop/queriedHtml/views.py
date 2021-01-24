from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.template import loader

from .models import Question, Modules

# this is an example of how I've displays the query result of the html page


def index(request):
    # Querying the database to get a list of modules(by mod_code as that is the primary key) that is in year 2
    modules_list = Modules.objects.filter(year=2)

    # creating a list to hold dictionaries of module codes and their summaries
    module_summaries = []

    for code in modules_list:
        module = Modules.objects.get(mod_code=code)
        summary = module.summary
        # mod_sum is a dictionary to store the mod_code and summary of each module
        mod_sum = {"module_code": code, "summary": summary}
        # module_summaries[code] = summary
        module_summaries.append(mod_sum)

    # dictionary of values you want to pass into the html page
    context = {'module_summaries': module_summaries}

    # using django shortcut that return a HttpResponse when called with a template and context
    return render(request, 'modules/index.html', context)

