from django.urls import path, include

from modulesApplication.views import *

app_name = 'modulesApplication'

# All the student urls
student_patterns = [
    path('all-modules/', student.all_modules, name="all-modules"),
    path('all-modules/<str:module>/', student.module_details, name="specific-module"),
    path('all-modules/sort/<int:sort>/', student.all_modules, name="filter-modules"),
    path('landing/', student.landing, name='student-landing'),
    path('choose-modules/', student.choose_modules, name='choose-modules'),
    path('choose-modules/<str:prog_code>/<str:stage>/', student.choose_specific_modules,
         name='choose-specific-modules'),
    path('foo/<str:prog_code>/', student.modules_by_programme, name='foo')
]
academic_patterns = []  # example
office_patterns = []  # example

urlpatterns = [
    path('', auths.index, name='index'),  # Just redirect to Student's index view for now
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),

]
