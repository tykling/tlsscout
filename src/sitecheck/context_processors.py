from .models import SiteCheck

def sitecheck_processor(request):
    return {
        'pendingchecks': SiteCheck.objects.filter(start_time__isnull=True).count(),
        'runningchecks': SiteCheck.objects.filter(start_time__isnull=False, finish_time__isnull=True).count(),
    }

