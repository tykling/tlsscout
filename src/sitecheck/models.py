from django.db import models

class SiteCheck(models.Model):
    site = models.ForeignKey('tlssite.Site', related_name='checks', on_delete=models.PROTECT)
    urgent = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)
    json_result = models.TextField(null=True, blank=True)
    status_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return "#%s %s: %s - %s (%s)" % (self.id, self.site.hostname, self.start_time, self.finish_time, self.status)

    class Meta:
        ordering = ['-finish_time']


### contains the results of a sitecheck, can contain multiple entries 
### per sitecheck if a hostname resolves to multiple IP addresses
class SiteCheckResult(models.Model):
    sitecheck = models.ForeignKey('SiteCheck', related_name='results', on_delete=models.PROTECT)
    serverip = models.GenericIPAddressField(unpack_ipv4=True, null=True)
    serverhostname = models.TextField(null=True)
    grade = models.CharField(max_length=2, null=True)
    status_message = models.TextField(null=True)
    status_details_message = models.TextField(null=True)

    def __str__(self):
        return self.grade if self.grade else self.status_message

