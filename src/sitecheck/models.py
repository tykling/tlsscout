from django.db import models
from tlssite.models import Site

class SiteCheck(models.Model):
    site = models.ForeignKey(Site, related_name='checks')
    urgent = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True)
    status = models.TextField(null=True)
    finish_time = models.DateTimeField(null=True)
    json_result = models.TextField(null=True)
    status_message = models.TextField(null=True)

    def __unicode__(self):
        return "#%s %s: %s - %s (%s)" % (self.id, self.site.hostname, self.start_time, self.finish_time, self.status)

    class Meta:
        ordering = ['-finish_time']


### contains the results of a sitecheck, can contain multiple entries 
### per sitecheck if a hostname resolves to multiple IP addresses
class SiteCheckResult(models.Model):
    sitecheck = models.ForeignKey(SiteCheck, related_name='results')
    serverip = models.GenericIPAddressField(unpack_ipv4=True, null=True)
    serverhostname = models.TextField(null=True)
    grade = models.CharField(max_length=2, null=True)
    status_message = models.TextField(null=True)
    status_details_message = models.TextField(null=True)

    def __unicode__(self):
        return self.grade if self.grade else self.status_message

