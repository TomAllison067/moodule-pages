from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class ConstraintType(models.TextChoices):
    CORE = 'CORE', _('Core')
    OPTS = 'OPTS', _('Option')
    STRAND = 'STRAND', _('Strand')
    DISC_ALT = 'DISC_ALT', _('DiscAlt')
    DISALLOWED = 'DISALLOWED', _('Disallowed')
    CREDITS = 'CREDITS', _('Credits')
    MAX_STRAND = 'MAX_STRAND', _('MaxStrand')


class OptionRule(models.Model):
    rule_id = models.AutoField(primary_key=True)
    prog_code = models.ForeignKey('Programme', models.DO_NOTHING, db_column='prog_code', null=False)
    entry_year = models.TextField(null=False)
    stage = models.IntegerField(null=False)
    constraint_type = models.TextField(choices=ConstraintType.choices, null=False)
    min_quantity = models.IntegerField(default=1)
    max_quantity = models.IntegerField(default=1)
    mod_code_pattern = models.TextField(null=False)


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.constraint_type not in ConstraintType:
            raise ValidationError("Invalid constraint_type.")

        super().save()
