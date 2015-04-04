from django.db import models
from django.contrib.auth.models import User
from group.models import Group
from taggit.models import Tag
from tlssite.models import Site


### sites
class SiteAlert(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site, null=True, related_name="alerts")


### tags
class TagAlert(models.Model):
    user = models.ForeignKey(User)
    tag = models.ForeignKey(Tag, null=True, related_name="alerts")


### groups
class GroupAlert(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True, related_name="alerts")


### alert history
class AlertHistory(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey(Site)
    html = models.TextField()

