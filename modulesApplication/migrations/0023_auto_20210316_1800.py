# Generated by Django 3.1.7 on 2021-03-16 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulesApplication', '0022_studentprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='entry_year',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='prog_code',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='stage',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='student_id',
            field=models.TextField(null=True),
        ),
    ]
