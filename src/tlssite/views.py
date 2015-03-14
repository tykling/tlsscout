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
from taggit.models import Tag


### list sites
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def site_list(request):
    ### get a list of sites
    sites = Site.objects.all()
    return render(request, 'tlssite/site_list.html', {
        'sites': sites,
    })


### add / edit site
@login_required
def site_add_edit(request,siteid=None):
    if not Group.objects.all().exists():
        return render(request, "tlssite/missing_group.html")

    if siteid:
        site = get_object_or_404(Site, id=siteid)
        form = SiteForm(request.POST or None, instance=site)
        template = 'tlssite/site_edit.html'
    else:
        form = SiteForm(request.POST or None)
        template = 'tlssite/site_add.html'

    if form.is_valid():
        site = form.save()
        return HttpResponseRedirect(reverse('group_details', kwargs={'groupid': site.group.id}))

    return render(request, template, {
        'form': form,
    })


### delete site
@login_required
def site_delete(request, siteid):
    ### if this site doesn't exist return 404
    site = get_object_or_404(Site, id=siteid)
    form = DeleteSiteForm(request.POST or None, instance=site)

    if form.is_valid():
        site.delete()
        return HttpResponseRedirect(reverse('site_list'))

    return render(request, 'tlssite/site_delete_confirm.html', {
        'form': form
    })


### site details
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def site_details(request, siteid):
    ### if this site doesn't exist return 404
    site = get_object_or_404(Site, id=siteid)
    
    return render(request, 'tlssite/site_details.html', {
        'site': site,
    })

### urgent site check
@login_required
def site_check(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    check = SiteCheck(site=site, urgent=True)
    check.save()
    return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': siteid}))


def tag_details(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    sites = Site.objects.filter(tags__slug=tagslug)
    
    return render(request, 'tlssite/tag_sitelist.html', {
        'sites': sites,
        'tag': tag,
    })

def tag_list(request):
    # tags = Tag.objects.all()
    ### XXX why the hell is it so retarded to get all tags
    tags = Site.objects.all()[0].tags.all()
    if Site.objects.all().count() > 1:
        for site in Site.objects.all():
            tags |= site.tags.all()
    ### remove duplicates
    tags = tags.distinct()
    return render(request, 'tlssite/tag_taglist.html', {
        'tags': tags
    })
