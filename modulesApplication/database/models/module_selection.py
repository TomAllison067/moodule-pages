from datetime import datetime

from django.db import models


class ModuleSelection(models.Model):
    student_id = models.TextField()
    stage = models.IntegerField(null=False)
    entry_year = models.TextField(default=str(datetime.now().year))
    status = models.TextField()
    programme = models.ForeignKey('Programme', models.CASCADE, default=None)
    date_requested = models.DateTimeField(null=True)
    last_modified = models.DateTimeField(null=True)
