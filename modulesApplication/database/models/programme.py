from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Programme(models.Model):
    """
    to help create model, you can use the extracted models from the sqlite database(file location below)
    need to find the model you require, in this case 'Programmes'
    use it as a reference, create a new file in the database/model folder, create model with the fields required
    be sure to check attributes of fields e.g check the null fields, make sure there is a primary key etc.

    file location: modulesApplication/resources/develop/models.py
    """
    prog_code = models.TextField(primary_key=True)
    title = models.TextField(unique=True)
    level = models.TextField()
    yini = models.BooleanField(default=False)
