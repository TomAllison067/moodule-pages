from django.db import models
from datetime import datetime

class ModuleSelection(models.Model):
    student_id = models.TextField()
    stage = models.IntegerField(null=False)
    entry_year = models.TextField(default=str(datetime.now().year))
    status = models.TextField()
