from django.db import models
from django.utils.translation import gettext_lazy as _

from modulesApplication.models import ModuleSelection


class LevelChoices(models.IntegerChoices):
    """Enum representing the level of this Module"""
    FOUR = 4, _('4')
    FIVE = 5, _('5')
    SIX = 6, _('6')
    SEVEN = 7, _('7')


class CreditsChoices(models.IntegerChoices):
    """Enum of the credits a Module is worth."""
    MINUS_ONE = -1, _('-1')
    FIFTEEN = 15, _('15')
    THIRTY = 30, _('30')
    SIXTY = 60, _('60')


class StatusChoices(models.TextChoices):
    """Enum representing the Module's status."""
    ACTIVE = 'ACTIVE', _('ACTIVE')
    DORMANT = 'DORMANT', _('DORMANT')
    WITHDRAWN = 'WITHDRAWN', _('WITHDRAWN')
    WONTRUN = 'WONTRUN', _('WONTRUN')


class Module(models.Model):
    """
    Represents a Module in the database, e.g. CS2815.
    """
    mod_code = models.CharField(blank=False, primary_key=True, max_length=10)
    """Primary key, e.g. 'CS2815'."""
    title = models.CharField(blank=True, null=True, max_length=255)
    """The title of the module."""
    level = models.IntegerField(blank=True, null=True, choices=LevelChoices.choices)
    """The level of this module. One of LevelChoices."""
    credits = models.IntegerField(blank=True, null=True, choices=CreditsChoices.choices)
    """How many credits the module is worth. One of CreditsChoices"""
    corequisites = models.TextField(blank=True, null=True, max_length=255)
    """A text field describing any corequisites."""
    prerequisites = models.TextField(blank=True, null=True, max_length=255)
    """A text field describing any prequisites."""
    banned_combinations = models.TextField(blank=True, null=True)
    """A text field describing any banned combinations."""
    learning_outcomes = models.TextField(blank=True, null=True)
    """A text field describing learning outcomes."""
    core_reading = models.TextField(blank=True, null=True)
    """A text field describing any core reading."""
    exam_format = models.TextField(blank=True, null=True)
    """A text field describing exam format."""
    summary = models.TextField(blank=True, null=True)
    """A text field summarising the module."""
    status = models.CharField(blank=True, null=True, choices=StatusChoices.choices, max_length=15)
    """The status of the module. One of StatusChoices."""
    project = models.BooleanField(blank=True, null=True)
    """Boolean. Whether the module is a project or not (?)."""
    selected_in = models.ManyToManyField(ModuleSelection)
    """ManyToMany field. A Module can be selected by many ModuleSelection objects."""

    def clean(self, *args, **kwargs):
        """Override of the ``clean()`` method to validate the mod_code. Called by ``self.save().``"""
        if self.mod_code is None or self.mod_code == "":
            raise ValueError
        super().clean()

    def save(self, *args, **kwargs):
        """Override of the save method to call ``self.clean()``, and check that a module has a mod_code.
        Most useful when importing potentially csv data.

        This also validates objects created with the ``Module.objects.create()`` method."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.mod_code, self.title)

    class Meta:
        ordering = ["mod_code"]
