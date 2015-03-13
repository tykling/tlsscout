from django.db import models
from group.models import Group

### contains all site definitions    
class Site(models.Model):
    group = models.ForeignKey(Group, related_name="sites")
    hostname = models.CharField(max_length=256)
    def __unicode__(self):
        return "%s (%s)" % (self.hostname, self.group)

