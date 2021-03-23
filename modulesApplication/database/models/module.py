from django.db import models
from django.utils.translation import gettext_lazy as _

from modulesApplication.models import ModuleSelection


class LevelChoices(models.IntegerChoices):
    FOUR = 4, _('4')
    FIVE = 5, _('5')
    SIX = 6, _('6')
    SEVEN = 7, _('7')


class CreditsChoices(models.IntegerChoices):
    MINUS_ONE = -1, _('-1')
    FIFTEEN = 15, _('15')
    THIRTY = 30, _('30')
    SIXTY = 60, _('60')


class StatusChoices(models.TextChoices):
    ACTIVE = 'ACTIVE', _('ACTIVE')
    DORMANT = 'DORMANT', _('DORMANT')
    WITHDRAWN = 'WITHDRAWN', _('WITHDRAWN')
    WONTRUN = 'WONTRUN', _('WONTRUN')


class Module(models.Model):
    """
    Represents a Module - eg cs2815 (hooray) or cs1860 (boo)
    """
    mod_code = models.CharField(blank=False, primary_key=True, max_length=10)
    title = models.CharField(blank=True, null=True, max_length=255)
    level = models.IntegerField(blank=True, null=True, choices=LevelChoices.choices)
    credits = models.IntegerField(blank=True, null=True, choices=CreditsChoices.choices)
    corequisites = models.TextField(blank=True, null=True, max_length=255)
    prerequisites = models.TextField(blank=True, null=True, max_length=255)
    banned_combinations = models.TextField(blank=True, null=True)
    learning_outcomes = models.TextField(blank=True, null=True)
    core_reading = models.TextField(blank=True, null=True)
    exam_format = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    status = models.CharField(blank=True, null=True, choices=StatusChoices.choices, max_length=15)
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
