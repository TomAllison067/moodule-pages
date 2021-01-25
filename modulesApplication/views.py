from django.shortcuts import render

from .models import Module


# Create your views here.
def index(request):
    # Querying the database to get a list of modules(by mod_code as that is the primary key) that starts with CS2
    modules_list = Module.objects.filter(mod_code__startswith='CS2')
    # creating a list to hold dictionaries of module codes and their summaries
    module_summaries = []

    for module in modules_list:
        code = module.mod_code
        if module.status == 'DORMANT':
            continue
        summary = module.summary
        # mod_sum is a dictionary to store the mod_code and summary of each module
        mod_sum = {"module_code": code, "summary": summary}
        # module_summaries[code] = summary
        module_summaries.append(mod_sum)

    # dictionary of values you want to pass into the html page
    context = {'module_summaries': module_summaries}

    # using django shortcut that return a HttpResponse when called with a template and context
    return render(request, 'modulesApplication/index.html', context)
