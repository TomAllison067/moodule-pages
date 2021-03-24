from datetime import datetime

from django.db import models


class ModuleSelection(models.Model):
    """A ModuleSelection is created by a student when they choose their modules.

    It specifies information about the student, and has a foreign key reference to their degree program.

    A Module can be selected via `a_module.selected_in.add(a_module_selection)`"""
    student_id = models.CharField(max_length=20)
    """The student's ID."""
    student_name = models.CharField(max_length=255)
    """The student's name."""
    stage = models.IntegerField(null=False)
    """The stage of the student's degree."""
    entry_year = models.CharField(default=str(datetime.now().year), max_length=4)
    """When the student began studying."""
    status = models.CharField(max_length=20)
    """The status of the selection - e.g., approved, pending, .etc."""
    programme = models.ForeignKey('Programme', models.CASCADE, default=None)
    """Foreign key to the Programme object this selection was made in context of."""
    date_requested = models.DateTimeField(null=True)
    """The date the selection was made."""
    last_modified = models.DateTimeField(null=True)
    """When the selection was last modified."""
    comments = models.TextField(null=True)
    """Text field of any comments provided."""
