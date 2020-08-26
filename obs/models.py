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

# this a possible PointSite class

# NOT USED


# this could be a replacement for ObservationType
# class ObsType(models.Model):
#     name = models.CharField(max_length=30)
#     icon = models.ImageField(upload_to='icons')
#     description = models.TextField()
#     author = models.ForeignKey(
#         'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)


class ObservationType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=30, null=True, blank=True,
                            help_text='No spaces, will be the name of the Vue component')
    icon = models.ImageField(upload_to='forms')
    description = models.TextField()
    author = models.ForeignKey(
        'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    xlsform = models.FileField(upload_to='forms', null=True, blank=True)
    form_json = JSONField(null=True, blank=True)
    script = models.TextField(null=True, blank=True)
    edit_html = models.TextField(null=True, blank=True)
    detail_html = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.xlsform:
            try:
                self.form_json = xlsconv.parse_xls(self.xlsform)
            except Exception as e:
                self.edit_html = "Error parsing form: %s" % e
                self.detail_html = "Error parsing form: %s" % e
            else:
                if not self.edit_html:
                    self.edit_html = self.generate_html('edit')
                if not self.detail_html:
                    self.detail_html = self.generate_html('detail')
        super().save(*args, **kwargs)

    def generate_html(self, template):
        try:
            html = xlsconv.render(
                xlsconv.html_context(self.form_json),
                XLSCONV_TEMPLATE % template,
            )
        except Exception as e:
            html = "Error generating HTML: %s" % e
        return html

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Project(models.Model):
    name = models.CharField(max_length=20, blank=True,
                            help_text='up to 20 characters')
    geography = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=2000, blank=True)

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

    # 'type' will be renamed 'obs_type' in production
    obs_type = models.ForeignKey(ObservationType, null=True, related_name='obs_type',
                                 on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, related_name='site_observations',
                             on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name='project', null=True, blank=True, default=1, on_delete=models.CASCADE)
    kv = JSONField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.obs_type, self.entered.date())

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
    body = models.TextField(blank=True)
