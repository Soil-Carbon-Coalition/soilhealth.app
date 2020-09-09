from django.db import models
from django.conf import settings

# this will be like a blog post, for a project. Not tied to a particular site.


class Post(models.Model):
    title = models.CharField(max_length=100, unique=False)
    body = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(
        'obs.Project', related_name='project_posts', null=True, blank=True, on_delete=models.SET_NULL)
    entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s (%s)' % (self.title, self.entered.date())

    class Meta:
        ordering = ['-id']


class PostComment(models.Model):
    subject = models.CharField(max_length=100, unique=False)
    body = models.TextField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(
        'users.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.CASCADE)
    entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.subject, self.author)

    class Meta:
        ordering = ['-id']
