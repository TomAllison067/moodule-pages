from django.db import models


class People(models.Model):
    """
    A class to represent a person, i.e, a member of the faculty.

    It is referenced by the CourseLeader class to link instructors to the modules they instruct.

    This corresponds to the 'people' table in the sqlite3 database.
    """
    id = models.TextField(primary_key=True)
    name = models.TextField()
    email = models.TextField()
