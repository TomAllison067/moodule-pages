import datetime

from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    """A database model to store information related to the student - e.g. their student ID"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.TextField(null=True)
    entry_year = models.TextField(null=True)
    prog_code = models.TextField(
        null=True)  # We can't use a foreign key here - some LDAP entries have multiple programmes..
    stage = models.SmallIntegerField(null=True)

    @staticmethod
    def populate_student_profile_from_ldap(user, student_id, entry_year, prog_code):
        print(user, student_id, entry_year, prog_code)
        profile, created = StudentProfile.objects.get_or_create(user=user)
        profile.student_id = student_id
        profile.entry_year = entry_year
        profile.prog_code = prog_code
        first_of_sept_in_entry_year = datetime.date(year=int(entry_year), month=9, day=1)
        now = datetime.date.today()
        days = now - first_of_sept_in_entry_year
        stage = days.days // 365 + 1
        print("STAGE is", stage)
        profile.stage = stage
        print(profile)
        profile.save()
