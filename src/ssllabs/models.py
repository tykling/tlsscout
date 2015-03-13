from django.db import models
from uuidfield import UUIDField
from sitecheck.models import SiteCheck

### API client state
class ApiClientState(models.Model):
    sleep_until = models.DateTimeField(null=True)
    max_concurrent_assessments = models.IntegerField()

### requestlog
class RequestLog(models.Model):
    sitecheck = models.ForeignKey(SiteCheck, related_name="requestlogs", null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    uuid = UUIDField()
    request_url = models.CharField(max_length=1000)
    request_headers = models.TextField()
    request_body = models.TextField(null=True)
    response_code = models.IntegerField(null=True)
    response_headers = models.TextField(null=True)
    response_body = models.TextField(null=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.id, self.request_url, self.datetime)

    class Meta:
        ordering = ['-datetime']
