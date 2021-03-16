from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect


@login_required
def login_redirect(request):
    """A view to handle redirecting upon login."""
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

