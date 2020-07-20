'''
Significant changes to models.py will occur once data from atlasbiowork is loaded for the transition. Likely the hierarchical parent-child data model for Observations will be discarded in favor of better query capability by site, etc. Soil sample obs can be extended with an analysis adjunct, or else correlated by site, sampleID, and date.
'''

from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField  # experimental
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class Site(models.Model):
    name = models.CharField(max_length=100, unique=False)
    geometry = models.GeometryField(srid=4326)
    accuracy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/sites/%i/" % self.id

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'sites'

# this a possible PointSite class

# NOT USED


class PointSite(models.Model):
    name = models.CharField(max_length=100, unique=False)
    point = PointField()

    @property
    def lat_lng(self):
        return list(getattr(self.point, 'coords', [])[::-1])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/pointsites/%i/" % self.id

    class Meta:
        ordering = ['-pk']


class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='forms')
    description = models.TextField()
    author = models.ForeignKey(
        'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    xlsform = models.FileField(upload_to='forms', null=True, blank=True)
    form_json = JSONField(null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    edit_html = models.TextField(null=True, blank=True)
    detail_html = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Project(models.Model):
    name = models.CharField(max_length=20, blank=True,
                            help_text='up to 20 characters')
    geography = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=2000, blank=True)

    project_coordinator = models.ForeignKey('users.CustomUser',
                                            null=True, blank=True,
                                            on_delete=models.SET_NULL)
    members_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Observation(models.Model):
    observer = models.ForeignKey('users.CustomUser',
                                 null=True, blank=True, related_name='observer',
                                 on_delete=models.SET_NULL)
    entered = models.DateTimeField(auto_now_add=True)
    # parentobs will be discarded in production
    parentobs = models.ForeignKey('self',
                                  null=True,
                                  blank=True,
                                  related_name='childobs',
                                  on_delete=models.CASCADE)
    # 'type' will be renamed 'obs_type' in production
    type = models.ForeignKey(ObservationType, null=True, related_name='type',
                             on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, related_name='site_observations',
                             on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name='project', null=True, blank=True, default=1, on_delete=models.CASCADE)
    kv = JSONField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.type.name, self.entered.date())

    def get_absolute_url(self):
        return "/observations/%i/" % self.id

    def get_ancestors(self):  # this is a recursive function!!!!
        if self.parentobs is None:
            return Observation.objects.none()
        return Observation.objects.filter(
            pk=self.parentobs.pk) | self.parentobs.get_ancestors()

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'observations'


class Comment(models.Model):
    author = models.ForeignKey('users.CustomUser',
                               null=True, blank=True, related_name='comment_author',
                               on_delete=models.CASCADE)
    observation = models.ForeignKey(Observation, null=True, related_name='observation',
                                    on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
