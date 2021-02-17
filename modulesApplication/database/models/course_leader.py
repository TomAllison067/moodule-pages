from django.db import models


class CourseLeader(models.Model):
    module = models.ForeignKey('Module', models.CASCADE)
    person = models.ForeignKey('People', models.CASCADE)
    leader = models.BooleanField()
    term = models.TextField()

    class Meta:
        unique_together = ('module', 'person')
