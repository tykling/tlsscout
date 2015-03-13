from django.db import models
from django.contrib.auth.models import User

### site groups
class Group(models.Model):
    name = models.CharField(max_length=50)
    interval_hours = models.PositiveIntegerField(default=24)
    publish = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.name

