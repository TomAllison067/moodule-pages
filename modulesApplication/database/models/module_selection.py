from datetime import datetime

from django.db import models


class ModuleSelection(models.Model):
    student_id = models.CharField(max_length=20)
    student_name = models.CharField(max_length=255)
    stage = models.IntegerField(null=False)
    entry_year = models.CharField(default=str(datetime.now().year), max_length=4)
    status = models.CharField(max_length=20)
    programme = models.ForeignKey('Programme', models.CASCADE, default=None)
    date_requested = models.DateTimeField(null=True)
    last_modified = models.DateTimeField(null=True)
    comments = models.TextField(null=True)
