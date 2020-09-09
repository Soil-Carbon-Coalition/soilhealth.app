'''
Significant changes to models.py will occur once data from atlasbiowork is loaded for the transition. Likely the hierarchical parent-child data model for Observations will be discarded in favor of better query capability by site, etc. Soil sample obs can be extended with an analysis adjunct, or else correlated by site, sampleID, and date.
'''

from django.contrib.gis.db import models
from django.contrib.gis.db.models import PointField  # experimental
from django.contrib.postgres.fields import JSONField
from django.conf import settings
import xlsconv

XLSCONV_TEMPLATE = settings.BASE_DIR + '/xlsconv_templates/%s.html'


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


class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=30, null=True, blank=True,
                            help_text='No spaces, will be the PascalCase name of the Vue component, such as PastureMove')
    icon = models.ImageField(upload_to='forms')
    description = models.TextField(
        max_length=200, null=True, blank=False, help_text='briefly describe purpose and function')
    author = models.ForeignKey(
        'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    xlsform = models.FileField(upload_to='forms', null=True, blank=True)
    form_json = JSONField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     if self.xlsform:
    #         try:
    #             self.form_json = xlsconv.parse_xls(self.xlsform)
    #         except Exception as e:
    #             self.edit_html = "Error parsing form: %s" % e
    #             self.detail_html = "Error parsing form: %s" % e
    #         else:
    #             if not self.edit_html:
    #                 self.edit_html = self.generate_html('edit')
    #             if not self.detail_html:
    #                 self.detail_html = self.generate_html('detail')
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Project(models.Model):
    name = models.CharField(max_length=25, blank=True,
                            help_text='25 characters max')
    geography = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=2000, blank=True, )
    members_only = models.BooleanField(
        default=True, help_text='In order to post observations, you must have joined and been accepted into that project. For members-only projects, only members can view the data.')
    obs_types = models.ManyToManyField(ObservationType, blank=True)

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
    # 'type' will be renamed 'obs_type' in production
    obs_type = models.ForeignKey(ObservationType, null=True, related_name='obs_type',
                                 on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, related_name='site_observations',
                             on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name='project_observations', null=True, blank=True, default=1, on_delete=models.CASCADE)
    # renamed from 'values'
    kv = JSONField(null=True, blank=True, help_text='must be valid JSON')

    def __str__(self):
        return '%s posted %s' % (self.obs_type, self.entered.date())

    def get_absolute_url(self):
        return "/observations/%i/" % self.id

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'observations'


class ObsComment(models.Model):
    author = models.ForeignKey('users.CustomUser',
                               null=True, blank=True, related_name='comment_author',
                               on_delete=models.CASCADE)
    observation = models.ForeignKey(Observation, null=True, related_name='observation',
                                    on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100, blank=True)
    body = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return '%s posted %s by %s' % (self.subject, self.entered.date(), self.author)
