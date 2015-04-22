from django.shortcuts import render
from eventlog.models import LogEntry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def EventList(request):
    all_events = LogEntry.objects.all().order_by('-datetime')
    paginator = Paginator(all_events, settings.EVENTS_PER_PAGE)
    
    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        events = paginator.page(paginator.num_pages)

    return render(request, 'event_list.html', {
        "events": events
    })

