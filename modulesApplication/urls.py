from django.urls import path, include

import modulesApplication.views.office_crud_views
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
    # As of 21/03/21, academic and office staff features have merged. - Keiru
]

# URLs for the generic crud views, to be included in the office urls.
crud_patterns = [
    path('view-all-programmes/', modulesApplication.views.office_crud_views.ProgrammeIndexView.as_view(),
         name='view-programmes'),
    path('update-programmes/<str:pk>', modulesApplication.views.office_crud_views.ProgrammeUpdate.as_view(),
         name='update-programmes'),
    path('view-course-leaders/', modulesApplication.views.office_crud_views.CourseLeaderListView.as_view(),
         name='view-course-leaders'),
    path('update-course-leader/<str:pk>', modulesApplication.views.office_crud_views.CourseLeaderUpdateView.as_view(),
         name='update-course-leader'),
    path('delete-course-leader/<str:pk>', modulesApplication.views.office_crud_views.CourseLeaderDeleteView.as_view(),
         name='delete-course-leader'),
    path('create-course-leader/', modulesApplication.views.office_crud_views.CourseLeaderCreateView.as_view(),
         name='create-course-leader'),
    path('staff-view-modules/', modulesApplication.views.office_crud_views.ModuleListView.as_view(),
         name='staff-view-modules'),
    path('staff-create-module/', modulesApplication.views.office_crud_views.ModuleCreateView.as_view(),
         name='staff-create-module'),
    path('staff-update-module/<str:pk>', modulesApplication.views.office_crud_views.ModuleUpdateView.as_view(),
         name='staff-update-module'),
    path('staff-delete-module/<str:pk>', modulesApplication.views.office_crud_views.ModuleDeleteView.as_view(),
         name='staff-delete-module'),
    path('staff-view-people/', modulesApplication.views.office_crud_views.PeopleListView.as_view(),
         name='staff-view-people'),
    path('staff-create-person/', modulesApplication.views.office_crud_views.PeopleCreateView.as_view(),
         name='staff-create-person'),
    path('staff-update-person/<str:pk>', modulesApplication.views.office_crud_views.PeopleUpdateView.as_view(),
         name='staff-update-person'),
    path('staff-delete-person/<str:pk>', modulesApplication.views.office_crud_views.PeopleDeleteView.as_view(),
         name='staff-delete-person'),
    path('staff-view-strands/', modulesApplication.views.office_crud_views.StrandListView.as_view(),
         name='staff-view-strands'),
    path('staff-create-strand/', modulesApplication.views.office_crud_views.StrandCreateView.as_view(),
         name='staff-create-strand'),
    path('staff-update-strand/<str:pk>', modulesApplication.views.office_crud_views.StrandUpdateView.as_view(),
         name='staff-update-strand'),
    path('staff-delete-strand/<str:pk>', modulesApplication.views.office_crud_views.StrandDeleteView.as_view(),
         name='staff-delete-strand')
]

office_patterns = [
    path('landing/', office.landing, name='office-landing'),
    path('selection-requests/', office.selection_requests, name='selection-requests'),
    path('archived-selection-requests/', office.archived_selection_requests, name='archived-selection-requests'),
    path('csvfiles/', office.csv, name="csv-downloads"),
    path('csvfiles/<str:model_class>/', office.csv_file, name="csv"),
    path('office/print_student_selections/', office.print_student_selections, name="print-student-selections"),
    path('', include(crud_patterns))  # CRUD urls
]

urlpatterns = [
    path('', index, name='index'),  # Redirect to homepage.
    path('login-redirect/', login_redirect, name='login-redirect'),
    path('student/', include(student_patterns)),
    path('academic/', include(academic_patterns)),
    path('office/', include(office_patterns)),
]
