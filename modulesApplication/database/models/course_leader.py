from django.db import models
from django.utils.translation import gettext_lazy as _


class TermChoices(models.TextChoices):
    """
    The term choices
    """
    TERM1 = '1', _('Term 1')
    TERM2 = '2', _('Term 2')
    BOTH = 'Both', _('Both')


class CourseLeader(models.Model):
    """This class links People to Modules. It specifies which people from the People table are instructors/leaders
    on a certain Module table.

    It also contains information about which term a module is in.

    This corresponds to the 'leaders' table in the sqlite3 database.
    """
    module = models.ForeignKey('Module', models.CASCADE)
    person = models.ForeignKey('People', models.CASCADE)
    leader = models.BooleanField()
    term = models.TextField(choices=TermChoices.choices, null=False)
    id = models.AutoField(primary_key=True)  # Automatic ID - needed since Django doesn't support composite keys

    class Meta:
        unique_together = ('module', 'person')  # The "composite key" though not officially supported
