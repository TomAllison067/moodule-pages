from django.urls import path, include

from modulesApplication.views import student, office, auths

app_name = 'modulesApplication'

# All the student urls
student_patterns = [

    path('all-modules/', student.all_modules, name="all-modules"),
    path('all-modules/<str:module>/', student.module_details, name="specific-module"),
    path('all-modules/sort/<int:sort>/', student.all_modules, name="filter-modules"),
    path('landing/', student.landing, name='student-landing'),
    path('choose-modules/', student.choose_modules, name='choose-modules'),
    path('choose-modules/submitted/<str:student_id>/<str:stage>', student.submitted, name='submitted'),
    path('choose-modules/<str:prog_code>/<str:stage>/',
         student.choose_specific_modules, name='choose-specific-modules'),
    path('choose-modules/submit/', student.submit_selection, name='submit-selection'),
    path('foo/<str:prog_code>/', student.modules_by_programme, name='foo')
]
academic_patterns = []  # example
office_patterns = [
    path('all/', office.landing, name="landing"),
    path('csvfiles/', office.csv_file, name="csv")
]  # example

urlpatterns = [
    path('', auths.index, name='index'),  # Redirect to homepage.
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),

]
