from django import template
register = template.Library()
from alert.models import GroupAlert

@register.filter
def get_group_alerting(group, user):
    try:
        groupalert = GroupAlert.objects.get(group=group, user=user.id)
        return groupalert.id
    except GroupAlert.DoesNotExist:
        return False

