from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from tlssite.models import Site
from django.contrib.auth.decorators import login_required, user_passes_test
from group.models import Group
from tlssite.forms import SiteForm, DeleteSiteForm
import re
from django.core.urlresolvers import reverse, reverse_lazy
from sitecheck.models import SiteCheck, SiteCheckResult
from tlsscout.decorators import logged_in_or_anon_allowed
from django.conf import settings
from ssllabs.wrappers import StartScan
from django.contrib import messages


### list sites
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def site_list(request):
    ### get a list of sites
    sites = Site.objects.all()
    return render(request, 'site_list.html', {
        'sites': sites,
    })


### add / edit site
@login_required
def site_add_edit(request,siteid=None):
    if not Group.objects.all().exists():
        return render(request, "missing_group.html")

    if siteid:
        site = get_object_or_404(Site, id=siteid)
        form = SiteForm(request.POST or None, instance=site)
        template = 'site_edit.html'
    else:
        site = None
        form = SiteForm(request.POST or None)
        template = 'site_add.html'

    if form.is_valid():
        site = form.save()
        if siteid:
            messages.success(request, 'The site "%s" has been updated.' % site.hostname)
        else:
            messages.success(request, 'The site "%s" has been created.' % site.hostname)
        return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': site.id}))

    return render(request, template, {
        'form': form,
        'site': site
    })


### delete site
@login_required
def site_delete(request, siteid):
    ### if this site doesn't exist return 404
    site = get_object_or_404(Site, id=siteid)
    form = DeleteSiteForm(request.POST or None, instance=site)

    if form.is_valid():
        site.delete()
        messages.success(request, 'The site "%s" has been deleted.' % site.hostname)
        return HttpResponseRedirect(reverse('site_list'))

    return render(request, 'site_delete_confirm.html', {
        'form': form,
        'site': site
    })


### site details
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def site_details(request, siteid):
    ### if this site doesn't exist return 404
    site = get_object_or_404(Site, id=siteid)

    return render(request, 'site_details.html', {
        'site': site,
    })


### urgent site check
@login_required
def site_check(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    if not start_urgent_check_ok(site):
        messages.error(request, 'A check of the site "%s" is already running, or an urgent check is already scheduled. Not scheduling a new urgent check.' % site.hostname)
    else:
        check = SiteCheck(site=site, urgent=True)
        check.save()
        messages.success(request, 'Scheduled an urgent check for the site "%s"' % site.hostname)
    return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': siteid}))


@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def site_nagios(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    latestcheck = site.checks.filter(finish_time__isnull=False).latest('finish_time')
    if latestcheck:
        results = [str(result) for result in latestcheck.results.all()]
        if results:
            return HttpResponse("/".join(results), content_type='text/plain')
    return HttpResponse("N/A", content_type='text/plain')


def start_urgent_check_ok(site):
    ### check if a check is already running for this site
    try:
        check = SiteCheck.objects.get(site=site, start_time__isnull=False, finish_time__isnull=True)
        return False
    except SiteCheck.DoesNotExist:
        pass
    
    ### check if an urgent check is already scheduled for this site
    try:
        check = SiteCheck.objects.get(site=site, start_time__isnull=True, finish_time__isnull=True, urgent=True)
        return False
    except SiteCheck.DoesNotExist:
        pass

    ### ok, go ahead and schedule a new urgent check for this site
    return True

