from django.db import models
from django.utils.translation import gettext_lazy as _


class TermChoices(models.TextChoices):
    """
    An enum representing what term the CourseLeader is running the related Module in.
    """
    TERM1 = '1', _('Term 1')
    TERM2 = '2', _('Term 2')
    BOTH = 'Both', _('Both')


class CourseLeader(models.Model):
    """
    A CourseLeader object relates a Person object to a Module object
    and defines who teaches a module, as well as what term the module is running in.
    """
    module = models.ForeignKey('Module', models.CASCADE)
    """The related Module object."""
    person = models.ForeignKey('People', models.CASCADE)
    """The related Person object."""
    leader = models.BooleanField()
    """Whether this CourseLeader is the primary leader of the Module or not."""
    term = models.CharField(choices=TermChoices.choices, null=False, max_length=6)
    """The term the module runs in. One of TermChoices."""
    id = models.AutoField(primary_key=True)  # Automatic ID - needed since Django doesn't support composite keys
    """Auto generated primary key integer. 
    
    The Meta inner class (see source code) specifies a unique_together contrainst between the
    module and person, since Django's ORM does not officially support composite keys."""

    class Meta:
        unique_together = ('module', 'person')  # The "composite key" though not officially supported

    def __str__(self):
        return 'Course Leader: {}'.format(self.person.name)
