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
    id = models.AutoField(primary_key=True)
    prog_code = models.ForeignKey('Programme', models.DO_NOTHING, db_column='prog_code', null=False)
    entry_year = models.TextField(null=False)
    stage = models.IntegerField(null=False)
    constraint_type = models.TextField(choices=ConstraintType.choices, null=False)
    min_quantity = models.IntegerField(default=1)
    max_quantity = models.IntegerField(default=1)
    mod_code_pattern = models.TextField(null=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Check that constraint_type is one of the choices
        if self.constraint_type not in ConstraintType:
            raise ValidationError("Invalid constraint_type.")
        super().save()

    @staticmethod
    def squash_core_modules(programme, entry_year, stage):
        """
        A static method to "squash" all of the core option rules for a given programme, entry year and stage
        into one single core option rule. It moves all mod_codes from the CORE rules for this programme/entry_year/stage
        into one single rule, and deletes the redundant rules.
        This means instead of having multiple CORE option rule per core module for
        each case, we can instead have one CORE option rule containing all of the modules in the rule's mod_code.
        :param programme: the Programme object who's core modules you wish to squash
        :param entry_year: the entry year of the programme
        :param stage: the stage of the programme who's core modules you wish to squash
        :return: True if all modules are squashed successfully
        """
        # Get all the core option rules for this programme, entry year and stage
        all_rules = OptionRule.objects.filter(prog_code=programme, entry_year=entry_year, stage=stage,
                                              constraint_type="CORE")
        count = all_rules.count()
        if not count:
            return
        mod_code_pattern = ""
        # Squash!
        separator = ""
        rules_squashed = 0
        for rule in all_rules:
            mod_code_pattern += (separator + rule.mod_code_pattern)
            separator = ","
            rules_squashed += 1
        if rules_squashed == count:
            all_rules.delete()
            OptionRule.objects.create(prog_code=programme, entry_year=entry_year, stage=stage,
                                      mod_code_pattern=mod_code_pattern,
                                      constraint_type="CORE",
                                      min_quantity=count,
                                      max_quantity=count)
            return True
        else:
            print("Unknown error: unable to squash all core modules for programme {}, entry year {} stage {}"
                  .format(programme.prog_code, entry_year, stage))
            return False

    @classmethod
    def squash_opts_modules(cls, programme, entry_year, stage, file):
        pass