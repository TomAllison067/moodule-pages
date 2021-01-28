from django.urls import path, include

from . import views

app_name = 'modulesApplication'

# All the student urls
student_patterns = [
    path('all-modules/', views.student.all_modules, name="all-modules"),
    path('all-modules/<str:module>/', views.student.module_details, name="specific-module"),
    path('landing/', views.student.landing, name='student-landing'),
    path('choose/', views.student.choose_modules, name='student-choose-modules'),
    #path('read-more/', views.student.read_more, name='student-read-more'),
]
academic_patterns = []  # example
office_patterns = []  # example

urlpatterns = [
    path('', views.student.index, name='index'),  # Just redirect to Student's index view for now
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns))
    
]
