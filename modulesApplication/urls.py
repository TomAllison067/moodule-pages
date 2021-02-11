from django.urls import path, include

from . import views

app_name = 'modulesApplication'

# All the student urls
student_patterns = [
    path('all-modules/', views.student.all_modules, name="all-modules"),
    path('all-modules/<str:module>/', views.student.module_details, name="specific-module"),
    path('all-modules/sort/<int:sort>/', views.student.all_modules, name="filter-modules"),
    path('landing/', views.student.landing, name='student-landing'),
    path('choose-modules/', views.student.choose_modules, name='choose-modules'),

]
academic_patterns = []  # example
office_patterns = []  # example

urlpatterns = [
    path('', views.index, name='index'),  # Just redirect to Student's index view for now
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),

    # Authentication links
    path('signin', views.index, name='signin'),
    path('signout', views.index, name='signout'),
]
