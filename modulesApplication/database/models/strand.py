from django.db import models


class Strands(models.Model):
    strand_id = models.AutoField(primary_key=True)
    mod_code = models.ForeignKey('Module', models.DO_NOTHING, db_column='mod_code', blank=False, null=False)
    strand = models.TextField(blank=False, null=False)

    class Meta:
        unique_together = ('mod_code', 'strand')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
