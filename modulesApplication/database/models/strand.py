from django.core.exceptions import ValidationError
from django.db import models, IntegrityError

from modulesApplication.database.models.module import Module


class Strands(models.Model):

    mod_code = models.ForeignKey('Module', models.DO_NOTHING, db_column='mod_code', blank=False, null=False)
    strand = models.TextField(blank=False, null=False)
    strand_id = models.AutoField(primary_key=True)

    class Meta:
        unique_together = ('mod_code', 'strand')

    def clean(self, *args, **kwargs):
        if self.strand_id is None:
            self.strand_id == Strands.objects.count() + 1
        super().clean()

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError:
            print("unable to add a strand")
            pass
        else:
            super().save(*args, **kwargs)
