from django.db import models
from django.contrib.auth.models import User
from group.models import Group
from taggit.models import Tag


### sites
class SiteAlert(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, null=True)


### tags
class TagAlert(models.Model):
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag, null=True)


### groups
class GroupAlert(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True)


### alert history
class AlertHistory(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site)
    html = models.TextField()

