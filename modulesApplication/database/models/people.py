from django.db import models


class People(models.Model):
    """
    A class to represent a person, i.e, a member of the faculty.

    It is referenced by the CourseLeader class to link instructors to the modules they instruct.

    This corresponds to the 'people' table in the sqlite3 database.
    """
    id = models.CharField(primary_key=True, max_length=5)  # Their initials
    name = models.CharField(max_length=255)  # Their full name
    email = models.CharField(max_length=255)  # Their email address

    def __str__(self):
        return self.name
