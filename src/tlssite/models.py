from django.db import models
from group.models import Group
from taggit.managers import TaggableManager

### contains all site definitions    
class Site(models.Model):
    group = models.ForeignKey(Group, related_name="sites")
    hostname = models.CharField(max_length=256, unique=True)
    last_change = models.DateTimeField(null=True)
    tags = TaggableManager(blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.hostname, self.group)

