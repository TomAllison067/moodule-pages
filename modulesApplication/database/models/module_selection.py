from django.db import models


class ModuleSelection(models.Model):
    student_id = models.TextField()
    stage = models.IntegerField(null=False)
    status = models.TextField()