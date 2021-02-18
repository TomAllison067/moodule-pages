from django.db import models


class CourseLeader(models.Model):
    """This class links People to Modules. It specifies which people from the People table are instructors/leaders
    on a certain Module table.

    It also contains information about which term a module is in.

    This corresponds to the 'leaders' table in the sqlite3 database.
    """
    module = models.ForeignKey('Module', models.CASCADE)
    person = models.ForeignKey('People', models.CASCADE)
    leader = models.BooleanField()
    term = models.TextField()
    id = models.AutoField(primary_key=True)  # Automatic ID - needed since Django doesn't support composite keys

    class Meta:
        unique_together = ('module', 'person')  # The "composite key" though not officially supported
