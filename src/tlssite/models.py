from django.db import models
from group.models import Group
from taggit.managers import TaggableManager
#from django.utils.functional import cached_property
from django.contrib.auth.models import User

### contains all site definitions    
class Site(models.Model):
    group = models.ForeignKey(Group, related_name="sites")
    hostname = models.CharField(max_length=256, unique=True)
    last_change = models.DateTimeField(null=True)
    tags = TaggableManager(blank=True)
    
    #@cached_property
    def get_alert_users(self):
        from alert.models import SiteAlert, TagAlert, GroupAlert
        sitealertusers = User.objects.filter(id__in=SiteAlert.objects.filter(site=self).values('user'))
        groupalertusers = User.objects.filter(id__in=GroupAlert.objects.filter(group=self.group).values('user'))
        tagalertusers = User.objects.filter(id__in=TagAlert.objects.filter(tag__in=[tag.id for tag in self.tags.all()]).values('user'))
        alertusers = sitealertusers | groupalertusers | tagalertusers
        return alertusers.distinct()

    def __unicode__(self):
        return "%s (%s)" % (self.hostname, self.group)

