# Generated by Django 3.1.5 on 2021-02-02 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulesApplication', '0003_auto_20210126_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('prog_code', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField(unique=True)),
                ('level', models.TextField(choices=[('BSC', "Bachelor's"), ('MSCI', "Master's")])),
                ('yini', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddConstraint(
            model_name='programme',
            constraint=models.CheckConstraint(check=models.Q(('level__iexact', 'bsc'), ('level__iexact', 'msci'), _connector='OR'), name='Valid degree level constraint'),
        ),
    ]
