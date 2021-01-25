from django.db import models


class Strands(models.Model):
    mod_code = models.ForeignKey('Module', models.DO_NOTHING,
                                 db_column='mod_code', blank=False, primary_key=True)
    strand = models.TextField(blank=True, null=True)
