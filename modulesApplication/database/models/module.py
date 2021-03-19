from django.db import models

from modulesApplication.models import ModuleSelection


class Module(models.Model):
    """
    Represents a Module - eg cs2815 (hooray) or cs1860 (boo)
    """
    mod_code = models.TextField(blank=False, primary_key=True)
    title = models.TextField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    corequisites = models.TextField(blank=True, null=True)
    prerequisites = models.TextField(blank=True, null=True)
    banned_combinations = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    project = models.BooleanField(blank=True, null=True)
    selected_in = models.ManyToManyField(ModuleSelection)

    def clean(self, *args, **kwargs):
        if self.mod_code is None or self.mod_code == "":
            raise ValueError
        super().clean()

    def save(self, *args, **kwargs):
        """Overriding the save() method to validate that new objects have a module code.
        This also validates objects created with the Module.objects.create() method"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.mod_code, self.title)

    class Meta:
        ordering = ["mod_code"]
