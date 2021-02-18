from django.db import models


class ModuleVariant(models.Model):
    """
    A class to map modules to their variants, e.g., CS2815 is a variant of CS2810.
    """
    major = models.ForeignKey('Module', models.CASCADE, related_name="major")  # The major module, e.g. CS2810
    minor = models.ForeignKey('Module', models.CASCADE,
                              related_name="minor")  # The minor module that is a variant of the major module
    id = models.AutoField(primary_key=True)  # Autogenerated ID in lieue of composite key

    class Meta:
        unique_together = ('major', 'minor')  # The "composite key" though not supported in Django
