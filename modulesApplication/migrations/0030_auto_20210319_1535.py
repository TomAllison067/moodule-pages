# Generated by Django 3.1.7 on 2021-03-19 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulesApplication', '0029_auto_20210319_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='exam_format',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='module',
            name='recommended_reading',
            field=models.TextField(blank=True, null=True),
        ),
    ]
