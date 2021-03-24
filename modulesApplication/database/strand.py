from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class StrandChoices(models.TextChoices):
    """Enum representing the different strands."""
    AI = 'AI', _('AI')
    IS = 'IS', _('IS')
    SE = 'SE', _('SE')
    DNS = 'DNS', _('DNS')


class Strands(models.Model):
    """Some modules may be on strands, e.g., CS2815 is on the Software Engineering strand. This relates modules to their
    strands if they should have one."""
    module = models.ForeignKey('Module', models.CASCADE, db_column='mod_code', blank=False, null=False)
    """Foreign key to the corresponding Module."""
    strand = models.CharField(blank=False, null=False, choices=StrandChoices.choices, max_length=5)
    """The strand - one of StrandChoices."""
    strand_id = models.AutoField(primary_key=True)
    """Auto-generated ID. The Meta subclass specifies a unique_together constraint between the module and strand, 
    as Django's ORM does not support composite keys."""

    class Meta:
        unique_together = ('module', 'strand')

    def clean(self, *args, **kwargs):
        super().clean()

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError:
            print("unable to add a strand")
            pass
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return "{} : {}".format(self.strand, self.module.mod_code)