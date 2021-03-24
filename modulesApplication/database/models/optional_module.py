from django.db import models


class OptionalModule(models.Model):
    """Maps Programmes to Modules to represent optional modules by programme."""
    id = models.AutoField(primary_key=True)
    """Auto-generated ID."""
    prog_code = models.ForeignKey('Programme', models.DO_NOTHING, db_column='prog_code', null=False)
    """Foreign key to the corresponding Programme."""
    mod_code = models.ForeignKey('Module', models.DO_NOTHING, db_column='mod_code', blank=False, null=False)
    """Foreign key to the corresponding Module."""

    class Meta:
        unique_together = ('prog_code', 'mod_code')
