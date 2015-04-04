from django import template
register = template.Library()
from alert.models import TagAlert

@register.filter
def get_tag_alerting(tag, user):
    try:
        tagalert = TagAlert.objects.get(tag=tag, user=user)
        return True
    except TagAlert.DoesNotExist:
        return False

