from django.db import models
from django.contrib.auth.models import User
from taggit.models import Tag

### sites
class SiteAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    site = models.ForeignKey('tlssite.Site', null=True, related_name="alerts", on_delete=models.PROTECT)


### tags
class TagAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, null=True, related_name="alerts", on_delete=models.PROTECT)


### groups
class GroupAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    group = models.ForeignKey('group.Group', null=True, related_name="alerts", on_delete=models.PROTECT)


### alert history
class AlertHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    datetime = models.DateTimeField(auto_now_add=True)
    site = models.ForeignKey('tlssite.Site', on_delete=models.PROTECT)
    html = models.TextField()

