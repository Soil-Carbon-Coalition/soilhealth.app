# Generated by Django 3.0.7 on 2020-07-09 01:49

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entered', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('body', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entered', models.DateTimeField(auto_now_add=True)),
                ('kv', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'observations',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ObservationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='forms')),
                ('description', models.TextField()),
                ('xlsform', models.FileField(blank=True, null=True, upload_to='forms')),
                ('form_json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('script', models.TextField(blank=True, null=True)),
                ('edit_html', models.TextField(blank=True, null=True)),
                ('detail_html', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PointSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='up to 20 characters', max_length=20)),
                ('geography', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, max_length=2000)),
                ('members_only', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('accuracy', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'sites',
                'ordering': ['-pk'],
            },
        ),
    ]