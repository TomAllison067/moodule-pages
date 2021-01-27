from django.urls import path, include

from . import views

app_name = 'modulesApplication'

# All the student urls
student_patterns = [
    path('all-modules/', views.student.all_modules, name="all-modules"),
    path('landing/', views.student.landing, name='student-landing'),
    path('choose/', views.student.choose_modules, name='student-choose-modules')
]
academic_patterns = []  # example
office_patterns = []  # example

urlpatterns = [
<<<<<<< HEAD
    path('', views.home, name='home'),
    path('AllModules.html', views.index, name='index'),
    path('StudentLandingPage.html', views.studentLanding, name='studentLanding'),
    path('StudentChooseModules.html', views.studentChooseModules, name='studentChooseModules'),
    path('ReadMore.html', views.readMore, name='ReadMore'),
=======
    path('', views.student.index, name='index'),  # Just redirect to Student's index view for now
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns))
>>>>>>> e56fa04dc78bd2ca1b094d7742886e12876643b4
]
