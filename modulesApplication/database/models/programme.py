from django.db import models


class Programme(models.Model):
    prog_code = models.TextField(primary_key=True)
    title = models.TextField()
    level = models.TextField()
