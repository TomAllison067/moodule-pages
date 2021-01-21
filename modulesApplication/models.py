from django.db import models

# Create your models here.
class Module(models.Model):
    mod_code = models.TextField(blank=True, null=False, primary_key=True)
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