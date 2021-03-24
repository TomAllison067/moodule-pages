import datetime

from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    """A database model to cache student information drawn from LDAP, avoiding repeat queries to the LDAP server
    each time we need this information.

    This is updated by LDAP each time a student logs in.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """The Django User object."""
    student_id = models.CharField(null=True, max_length=20)
    """The student's ID."""
    entry_year = models.CharField(null=True, max_length=4)
    """The year they began their studies."""
    prog_code = models.CharField(
        null=True, max_length=10)  # We can't use a foreign key here - some LDAP entries have multiple programmes..
    """String of student's programme code. May be null if LDAP entry is incorrect, e.g. there are two."""
    stage = models.SmallIntegerField(null=True)
    """The student's degree stage. Calculated on login from their entry year."""

    @staticmethod
    def populate_student_profile_from_ldap(user, student_id, entry_year, prog_code):
        """Populates this profile given the user object, their student ID, entry_year and programme code, drawn from
        LDAP on login."""
        profile, created = StudentProfile.objects.get_or_create(user=user)
        profile.student_id = student_id
        profile.entry_year = entry_year
        profile.prog_code = prog_code
        first_of_sept_in_entry_year = datetime.date(year=int(entry_year), month=9, day=1)
        now = datetime.date.today()
        days = now - first_of_sept_in_entry_year
        stage = days.days // 365 + 1
        profile.stage = stage
        profile.save()
