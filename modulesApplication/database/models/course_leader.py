from django.db import models


class CourseLeader(models.Model):
    mod_code = models.ForeignKey('Module', models.CASCADE)
    initials = models.ForeignKey('People', models.CASCADE)
    leader = models.BooleanField()
    term = models.TextField()

    class Meta:
        unique_together = ('mod_code', 'initials')