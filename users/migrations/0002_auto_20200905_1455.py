# Generated by Django 3.0.7 on 2020-09-05 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('obs', '0005_auto_20200905_1455'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstatus',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_user', to='obs.Project'),
        ),
        migrations.AlterField(
            model_name='userstatus',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
