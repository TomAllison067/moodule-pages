import datetime
import re

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
def choose_degree_and_stage(request):
    if request.method == "POST":
        prog_code = request.POST.get('programme')
        stage = request.POST.get('stage')
        entry_year = request.POST.get('entry_year') or '2019'
        if prog_code is None or stage is None:
            return HttpResponseRedirect(reverse("modulesApplication:choose-degree-and-stage"))
        url = reverse('modulesApplication:choose-modules',
                      kwargs={'prog_code': prog_code,
                              'stage': stage,
                              'entry_year': entry_year})
        return HttpResponseRedirect(url)
    return render(request, 'modulesApplication/student/ChooseDegreeAndStage.html')


@login_required
def choose_modules(request, prog_code, stage, entry_year):
    if request.method == "GET":
        try:
            info = factory.get_programme_info(prog_code, stage=int(stage), entry_year=entry_year)
        except Programme.DoesNotExist:
            raise Http404
        context = {'info': info,
                   'stage': "stage{}".format(stage),
                   }
        return render(request, 'modulesApplication/student/ChooseModules.html', context=context)
    if request.method == "POST":
        # Get all the arguments from the form
        student_id = request.user.id if request.POST.get('student-id') == "" else request.POST.get('student-id')
        mod_codes = set(request.POST.getlist('module-selections'))
        programme = Programme.objects.get(pk=prog_code)
        if SelectionValidator(prog_code, stage, entry_year, mod_codes).validate():  # If the selection is valid
            ModuleSelection.objects.filter(student_id=student_id).delete()
            student_name = request.user.first_name + ' ' + request.user.last_name
            selection = ModuleSelection.objects.create(
                student_id=student_id, student_name=student_name, stage=stage, entry_year=entry_year, status="PENDING",
                programme=programme,
                date_requested=datetime.datetime.now())
            for m in mod_codes:
                module = Module.objects.get(mod_code=m)
                module.selected_in.add(selection)
            return HttpResponseRedirect(reverse("modulesApplication:submitted",
                                                kwargs={'student_id': student_id,
                                                        'stage': stage,
                                                        'entry_year': entry_year,
                                                        'prog_code': prog_code}))
        else:
            messages.add_message(request, messages.ERROR, "ERROR: Invalid selection.")
            return HttpResponseRedirect(reverse("modulesApplication:choose-modules",
                                                kwargs={'prog_code': prog_code,
                                                        'stage': stage,
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
    try:
        student_id = request.user.ldap_user.attrs.get('extensionAttribute3')[0]  # Ignore the warning for now..
    except AttributeError:
        student_id = request.user.id
    selection = get_object_or_404(
        ModuleSelection,
        student_id=student_id
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


@login_required
def choice_pathway(request):
    """Handles a user wanting to choose their modules. It attempts to derive the student's degree and stage from LDAP,
    and take them straight to the correct module choice form if successful."""
    # Attempt to derive the degree (this should probably just be cached... refactoring todo!)
    if hasattr(request.user, 'ldap_user'):
        print("HERE!!!")
        potential_prog_codes = []
        for value in request.user.ldap_user.attrs.get('memberOf'):
            regex = re.search("Programme \d*", value)
            if regex:
                potential_prog_codes.append(regex.group(0))
        print("list: \n", potential_prog_codes)
        if len(potential_prog_codes) != 1:
            # People may have multiple programmes in LDAP.. we don't know which is correct, so give them the choice
            # Todo: Handle this better somehow as part of refactoring ldap attrs into related db model
            return HttpResponseRedirect(reverse('modulesApplication:choose-degree-and-stage'))
        prog_code = potential_prog_codes[0].split(' ')[1]

        # Derive the entry year and stage TODO sort this out in the related info db model to come...
        entry_year = request.user.ldap_user.attrs.get('whenCreated')[0][:4]
        first_of_sept_in_entry_year = datetime.date(year=int(entry_year), month=9, day=1)
        now = datetime.date.today()
        days = now - first_of_sept_in_entry_year
        stage = days.days // 365 + 1

        return HttpResponseRedirect(reverse('modulesApplication:choose-modules',
                                            kwargs={'prog_code': prog_code,
                                                    'stage': stage,
                                                    'entry_year': entry_year}
                                            ))
    else:  # If no ldap user for some reason.. (eg if you're a dev & signed into django account), be given the choice
        return HttpResponseRedirect(reverse('modulesApplication:choose-degree-and-stage'))
