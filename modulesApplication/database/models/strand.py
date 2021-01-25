from django.db import models


class Strands(models.Model):
    mod_code = models.ForeignKey('Module', models.DO_NOTHING,
                                 db_column='mod_code', blank=False, primary_key=True)
    strand = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        for module in Strands.objects.all():
            if self.mod_code == module.mod_code:
                if self.strand == module.strand:
                    print(self.mod_code, "is already in database.")
                else:
                    print(self.mod_code,
                          "is already taken in this database. "
                          "Unable to add this record, try deleting previous record before adding.")
                return 0
        self.full_clean()
        super().save(*args, **kwargs)
