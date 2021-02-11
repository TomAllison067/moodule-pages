from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    #template_name = 'modulesApplication/index.html'
    #return render(request, template_name)
    context = initialize_context(request)
    return render(request, 'tutorial/home.html', context)



#Authentication views:

def initialize_context(request):
  context = {}
  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context