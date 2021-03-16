from modulesApplication.database.models.module_selection import ModuleSelection
from modulesApplication.database.models.module import Module
from modulesApplication.database.models.strand import Strands
from modulesApplication.database.models.programme import Programme
from modulesApplication.database.models.option_rule import OptionRule
from modulesApplication.database.models.optional_module import OptionalModule
from modulesApplication.database.models.people import People
from modulesApplication.database.models.course_leader import CourseLeader
from modulesApplication.database.models.module_variants import ModuleVariant
from modulesApplication.database.models.student_profile import StudentProfile
""" 
We have created a separate file for each model and place it into a folder(file location below) 
so after we create a new model in that folder we must import it into this file as when we run the application 
looks for models in this file

file location: modulesApplication/database/models/  
"""
