from django.shortcuts import render
from sitecheck.models import SiteCheck
from django.utils.safestring import mark_safe

def metrics(request):
    metricsdict = {}

    # add sitechecks stats
    metricsdict['tlsscout_sitechecks_total'] = {
        'help': 'TLSScout number of SiteChecks',
        'type': 'gauge',
        'values': [
            {
                'labels': mark_safe('{state="pending"}'),
                'value': SiteCheck.objects.filter(start_time__isnull=True).count(),
            },
            {
                'labels': mark_safe('{state="running"}'),
                'value': SiteCheck.objects.filter(start_time__isnull=False, finish_time__isnull=True).count(),
            },
            {
                'labels': mark_safe('{state="finished"}'),
                'value': SiteCheck.objects.filter(finish_time__isnull=False).count(),
            },
        ],
    }

    response = render(request, 'prometheus.html.j2', {'metrics': metricsdict})
    response['content-type'] = "text/plain"
    return response

