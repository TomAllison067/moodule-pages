"""
Views handling the user's entry point into the application.
"""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.shortcuts import render


def index(request):
    """
    Displays the index page.
    """
    return render(request, 'modulesApplication/main/index.html')


@login_required
def login_redirect(request):
    """A view to handle redirection upon login.

    Redirects students to the ``student-landing`` view, and staff to the ``staff-landing`` view.
    """
    try:
        user_group = Group.objects.get(user=request.user).name
        if user_group == "Students":
            return redirect('modulesApplication:student-landing')
        elif user_group == "Staff":
            return redirect('modulesApplication:office-landing')
        else:
            return redirect('modulesApplication:index')
    except Group.DoesNotExist:
        return redirect('modulesApplication:index')
