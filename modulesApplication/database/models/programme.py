from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class DegreeLevel(models.TextChoices):
    """
    The valid degree levels.
    """
    BACHELORS = 'BSC', _('Bachelor\'s')
    MASTERS = 'MSCI', _('Master\'s')


class Programme(models.Model):
    """
    A data model representing a degree program, eg 'BSc Computer Science'.
    It has four fields:
    prog_code: A string of the programme code, the primary key.
    title: The title of the degree programme.
    level: The level of study, e.g. BS or MSc
    yini: Boolean, true if this course contains a Year in Industry placement.
    This is very much simplified in comparison to the equivalent model in the example database, as we simply don't
    need most of those fields for our purposes.
    """

    prog_code = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(unique=True, max_length=255)
    level = models.CharField(choices=DegreeLevel.choices, max_length=10)  # Choices validated at model level
    yini = models.BooleanField(default=False)

    def clean(self):
        """
        Validates the object at the model level.
        Called when a ModelForm validates the model, or of course when we want to call it ourselves.
        """
        level = self.level.upper()
        if level not in [level[0] for level in DegreeLevel.choices]:
            raise ValidationError("Invalid degree level. Valid levels are BSC or MSCI.")
        else:
            self.level = level

    class Meta:
        """
        Model constraints at the database level.
        """
        constraints = [
            models.CheckConstraint(
                check=(models.Q(level__iexact="bsc") | models.Q(level__iexact="msci")),
                name="Valid degree level constraint"
            )
        ]
