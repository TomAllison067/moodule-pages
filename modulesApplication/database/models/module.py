from django.db import models
from modulesApplication.models import ModuleSelection


class Module(models.Model):
    """
    Represents a Module - eg cs2815 (hooray) or cs1860 (boo)
    """
    mod_code = models.TextField(blank=False, primary_key=True)
    jacs_code = models.TextField(blank=True, null=True)
    hecos_code = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    short_title = models.TextField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    department = models.TextField(blank=True, null=True)
    with_effect_from = models.TextField(blank=True, null=True)
    availability_terms = models.TextField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    corequisites = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    banned_combinations = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    notional_learning_hours = models.TextField(blank=True, null=True)
    books_to_purchase = models.TextField(blank=True, null=True)
    core_reading = models.TextField(blank=True, null=True)
    exam_format = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    project = models.BooleanField(blank=True, null=True)
    lab_hours = models.IntegerField(blank=True, null=True)
    deg_progs = models.TextField(blank=True, null=True)
    selected_in = models.ManyToManyField(ModuleSelection)

    def clean(self, *args, **kwargs):
        if self.mod_code is None or self.mod_code == "":
            raise ValueError
        if self.lab_hours == "":
            self.lab_hours = None
        super().clean()

    def save(self, *args, **kwargs):
        """Overriding the save() method to validate that new objects have a module code.
        This also validates objects created with the Module.objects.create() method"""
        self.full_clean()
        super().save(*args, **kwargs)

