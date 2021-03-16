from django.urls import path, include

from modulesApplication.views import *

app_name = 'modulesApplication'

# All the student urls
student_patterns = [
    path('all-modules/', student.all_modules, name="all-modules"),
    path('all-modules/<str:module>/', student.module_details, name="specific-module"),
    path('all-modules/sort/<int:sort>/', student.all_modules, name="filter-modules"),
    path('landing/', student.landing, name='student-landing'),
    path('choose-degree-and-stage/', student.choose_degree_and_stage, name='choose-degree-and-stage'),
    path('choose-modules/<str:prog_code>/<str:stage>/<str:entry_year>',
         student.choose_modules, name='choose-modules'),
    path('choose-modules/submitted/<str:student_id>/<str:prog_code>/<str:entry_year>/<str:stage>',
         student.submitted, name='submitted'),
    path('my-selection', student.my_selection, name='my-selection'),
    path('choice-pathway', student.choice_pathway, name='choice-pathway')
]

academic_patterns = [
    path('landing/', academic.landing, name='academic-landing'),
    path('selection-requests/', academic.selection_requests, name='academic-selection-requests'),
    path('view-all-programmes/', academic.ProgrammeIndexView.as_view(), name='view-programmes'),
    path('update-programmes/<str:pk>', academic.ProgrammeUpdate.as_view(), name='update-programmes')
]

office_patterns = [
    path('landing/', office.landing, name='office-landing'),
    path('selection-requests/', office.selection_requests, name='selection-requests'),
    path('archived-selection-requests/', office.archived_selection_requests, name='archived-selection-requests'),
    path('csvfiles/', office.csv, name="csv-downloads"),
    path('csvfiles/<str:model_class>/', office.csv_file, name="csv"),
    path('office/print_student_selections/', office.print_student_selections, name="print-student-selections")
]

urlpatterns = [
    path('', index, name='index'),  # Redirect to homepage.
    path('login-redirect/', login_redirect, name='login-redirect'),
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),
]
