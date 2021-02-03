from django.core.exceptions import ValidationError
from django.db import models


class Strands(models.Model):

    module = models.ForeignKey('Module', models.DO_NOTHING, db_column='mod_code', blank=False, null=False)
    strand = models.TextField(blank=False, null=False)
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
