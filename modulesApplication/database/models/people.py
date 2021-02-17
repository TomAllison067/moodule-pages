from django.db import models


class People(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField()
    email = models.TextField()