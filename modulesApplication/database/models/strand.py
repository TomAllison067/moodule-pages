from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class StrandChoices(models.TextChoices):
    AI = 'AI', _('AI')
    IS = 'IS', _('IS')
    SE = 'SE', _('SE')
    DNS = 'DNS', _('DNS')


class Strands(models.Model):
    module = models.ForeignKey('Module', models.CASCADE, db_column='mod_code', blank=False, null=False)
    strand = models.TextField(blank=False, null=False, choices=StrandChoices.choices)
    strand_id = models.AutoField(primary_key=True)

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