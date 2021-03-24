"""
This module simply imports data model classes from the database package, for ease of organisation.

models location: modulesApplication/database/
"""

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

