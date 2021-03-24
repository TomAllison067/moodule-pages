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

    This is very much simplified in comparison to the equivalent model in the example database, as we simply don't
    need most of those fields for our purposes.
    """
    prog_code = models.CharField(primary_key=True, max_length=255)
    """Primary key, e.g. '1067'."""
    title = models.CharField(unique=True, max_length=255)
    """The degree title e.g., 'BSc Computer Science'."""
    level = models.CharField(choices=DegreeLevel.choices, max_length=10)
    """What level the degree programme is. One of BSC or MSCI."""
    yini = models.BooleanField(default=False)
    """Boolean. Whether this Programme contains a Year in Industry."""

    def clean(self):
        """
        Override to validate the level. Useful when importing CSV data.
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
