from django.db import models
from group.models import Group
from taggit.managers import TaggableManager
from django.utils.functional import cached_property

### contains all site definitions    
class Site(models.Model):
    group = models.ForeignKey(Group, related_name="sites")
    hostname = models.CharField(max_length=256, unique=True)
    last_change = models.DateTimeField(null=True)
    tags = TaggableManager(blank=True)

    #@cached_property
    def recursive_alerting(self, user):
        from alert.models import SiteAlert, TagAlert, GroupAlert

        ### is alerting enabled for this site?
        try:
            sitealert = SiteAlert.objects.get(site=self, user=user)
            return True
        except SiteAlert.DoesNotExist:
            pass

        ### is alerting enabled for the sites group?
        try:
            groupalert = GroupAlert.objects.get(group=self.group)
            return True
        except GroupAlert.DoesNotExist:
            pass

        ### is alerting enabled for any of this sites tags?
        for tag in self.tags.all():
            try:
                tagalert = TagAlert.objects.get(tag=tag, user=user)
                return True
            except TagAlert.DoesNotExist:
                pass

        ### neither site, group or tag alerting for this site
        return False

    def __unicode__(self):
        return "%s (%s)" % (self.hostname, self.group)

