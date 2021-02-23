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
    path('choose-modules/submitted/<str:student_id>/<str:prog_code>/<str:entry_year>/<str:stage>',
         student.submitted, name='submitted'),
    path('choose-modules/<str:prog_code>/<str:stage>/<str:entry_year>',
         student.choose_specific_modules, name='choose-specific-modules'),
    path('choose-modules/submit/', student.submit_selection, name='submit-selection'),
    path('my-selection', student.my_selection, name='my-selection')
]

academic_patterns = []  # example

office_patterns = [
    path('landing/', office.landing, name='office-landing'),
    path('csvfiles/', office.csv, name="csv-downloads"),
    path('csvfiles/<str:model_class>/', office.csv_file, name="csv")
]

urlpatterns = [
    path('', index, name='index'),  # Redirect to homepage.
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),
]
