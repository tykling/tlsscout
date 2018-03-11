from django.db import models

### configuration groups
class Group(models.Model):
    name = models.CharField(max_length=50)
    interval_hours = models.PositiveIntegerField(default=24)
    publish = models.BooleanField(default=True)
    ignore_name_mismatch = models.BooleanField(default=False)

    def __str__(self):
        return self.name

