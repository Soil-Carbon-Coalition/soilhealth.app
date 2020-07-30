# Generated by Django 3.0.7 on 2020-07-30 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obs', '0002_auto_20200708_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_coordinator',
        ),
        migrations.AddField(
            model_name='project',
            name='obs_types',
            field=models.ManyToManyField(to='obs.ObservationType'),
        ),
    ]
