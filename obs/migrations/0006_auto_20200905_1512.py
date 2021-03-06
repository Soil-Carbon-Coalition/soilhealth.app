# Generated by Django 3.0.7 on 2020-09-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('obs', '0005_auto_20200905_1455'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='observationtype',
            name='detail_html',
        ),
        migrations.RemoveField(
            model_name='observationtype',
            name='edit_html',
        ),
        migrations.RemoveField(
            model_name='observationtype',
            name='script',
        ),
        migrations.AlterField(
            model_name='observationtype',
            name='description',
            field=models.TextField(help_text='briefly describe purpose and function', max_length=200, null=True),
        ),
    ]
