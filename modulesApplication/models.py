from django.db import models


# Create your models here.
class Module(models.Model):
    mod_code = models.TextField(blank=False, null=False, primary_key=True)
    title = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    contact_hours = models.IntegerField(blank=True, null=True)
    exams = models.IntegerField(blank=True, null=True)
    practical = models.IntegerField(blank=True, null=True)
    coursework = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    outcomes = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Overriding the save() method to validate that new objects have a module code.
        This also validates objects created with the Module.objects.create() method"""
        if self.mod_code is None or self.mod_code == "":
            raise ValueError
        else:
            super().save(*args, **kwargs)
