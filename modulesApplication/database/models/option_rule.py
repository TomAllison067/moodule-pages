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

    def group_core(self):
        for rule in OptionRule.objects.all():
            if self.prog_code == rule.prog_code and self.entry_year == rule.entry_year and self.stage == rule.stage:
                rule.mod_code_pattern = rule.mod_code_pattern + ", " + self.mod_code_pattern
                rule.save(force_update=True)
                return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Check that constraint_type is one of the choices
        if self.constraint_type not in ConstraintType:
            raise ValidationError("Invalid constraint_type.")

        # groups together all the core modules
        if self.constraint_type == "CORE" and not force_update:
            if self.group_core():
                return
        super().save()
