from django import template
register = template.Library()
from alert.models import SiteAlert

@register.filter
def get_site_alerting(site, user):
    try:
        sitealert = SiteAlert.objects.get(site=site, user=user)
        return True
    except SiteAlert.DoesNotExist:
        return False

