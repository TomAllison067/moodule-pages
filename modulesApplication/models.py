from modulesApplication.database.module_selection import ModuleSelection
from modulesApplication.database.course_leader import CourseLeader
from modulesApplication.database.module import Module
from modulesApplication.database.module_variants import ModuleVariant
from modulesApplication.database.option_rule import OptionRule
from modulesApplication.database.optional_module import OptionalModule
from modulesApplication.database.people import People
from modulesApplication.database.programme import Programme
from modulesApplication.database.strand import Strands
from modulesApplication.database.student_profile import StudentProfile


""" 
We have created a separate file for each model and place it into a folder(file location below) 
so after we create a new model in that folder we must import it into this file as when we run the application 
looks for models in this file

file location: modulesApplication/database/models/  
"""
