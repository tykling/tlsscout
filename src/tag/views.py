from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from tlssite.models import Site
from django.contrib.auth.decorators import login_required, user_passes_test
from tlsscout.decorators import logged_in_or_anon_allowed
from django.core.urlresolvers import reverse, reverse_lazy
from taggit.models import Tag
from django.contrib import messages
from sitecheck.models import SiteCheck
from tlssite.views import start_urgent_check_ok


@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def tag_details(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    sites = Site.objects.filter(tags__slug=tagslug)
    
    return render(request, 'tag_sitelist.html', {
        'sites': sites,
        'tag': tag,
    })


@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def tag_list(request):
    # tags = Tag.objects.all()
    ### XXX why the hell is it so retarded to get all tags?
    if Site.objects.all().count() == 0:
        tags = None
    else:
        tags = Site.objects.all()[0].tags.all()
        if Site.objects.all().count() > 1:
            for site in Site.objects.all():
                tags |= site.tags.all()
        ### remove duplicates
        tags = tags.distinct()
    return render(request, 'tag_taglist.html', {
        'tags': tags
    })


### urgent tag check
@login_required
def tag_check(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    sites = Site.objects.filter(tags__slug=tagslug)
    checkcounter=0
    for site in sites:
        if not start_urgent_check_ok(site):
            messages.error(request, 'A check of the site %s is already running, or an urgent check is already scheduled. Not scheduling a new urgent check.' % site.hostname)
        else:
            check = SiteCheck(site=site, urgent=True)
            check.save()
            checkcounter += 1
    if checkcounter > 0:
        messages.success(request, 'Scheduled an urgent check for %s sites tagged with %s' % (checkcounter, tagslug))
    else:
        messages.error(request, 'No new urgent checks scheduled')
    return HttpResponseRedirect(reverse('tag_details', kwargs={'tagslug': tagslug}))

