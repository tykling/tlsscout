from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from tlssite.models import Site
from group.models import Group
from alert.models import SiteAlert, TagAlert, GroupAlert
from alert.forms import EnableSiteAlertForm, DisableSiteAlertForm, EnableGroupAlertForm, DisableGroupAlertForm, EnableTagAlertForm, DisableTagAlertForm
from taggit.models import Tag

def enable_site_alert(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    form = EnableSiteAlertForm(request.POST or None)

    # check if alerting is already enabled for this site
    try:
        alert = SiteAlert.objects.get(user=request.user, site=site)
        messages.error(request, 'Alerting is already enabled for the site %s' % site.hostname)
    except SiteAlert.DoesNotExist:
        if form.is_valid():
            alert = SiteAlert(user=request.user, site=site)
            alert.save()
            messages.success(request, 'Alerting has now been enabled for the site %s' % site.hostname)
            return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': site.id}))

    return render(request, 'alert/enable_site_alert.html', {
        'form': form,
        'site': site
    })


def disable_site_alert(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    alert = get_object_or_404(SiteAlert, site=site, user=request.user)
    form = DisableSiteAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the site %s' % site.hostname)
        return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': site.id}))

    return render(request, 'alert/disable_site_alert.html', {
        'form': form,
        'site': site
    })


def enable_tag_alert(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    form = EnableTagAlertForm(request.POST or None)

    # check if alerting is already enabled for this tag
    try:
        alert = TagAlert.objects.get(user=request.user, tag=tag)
        messages.error(request, 'Alerting is already enabled for the tag %s' % tag)
    except TagAlert.DoesNotExist:
        if form.is_valid():
            alert = TagAlert(user=request.user, tag=tag)
            alert.save()
            messages.success(request, 'Alerting has now been enabled for the tag %s' % tag)
            return HttpResponseRedirect(reverse('tag_list'))

    return render(request, 'alert/enable_tag_alert.html', {
        'form': form,
        'tag': tag
    })

def disable_tag_alert(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    alert = get_object_or_404(TagAlert, tag=tag, user=request.user)
    form = DisableTagAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the tag %s' % tag)
        return HttpResponseRedirect(reverse('tag_list'))

    return render(request, 'alert/disable_tag_alert.html', {
        'form': form,
        'tag': tag
    })


def enable_group_alert(request, groupid):
    group = get_object_or_404(Group, id=groupid)
    form = EnableGroupAlertForm(request.POST or None)

    # check if alerting is already enabled for this group
    try:
        alert = GroupAlert.objects.get(user=request.user, group=group)
        messages.error(request, 'Alerting is already enabled for the group %s' % group.name)
    except GroupAlert.DoesNotExist:
        if form.is_valid():
            alert = GroupAlert(user=request.user, group=group)
            alert.save()
            messages.success(request, 'Alerting has now been enabled for the group %s' % group.name)
            return HttpResponseRedirect(reverse('group_details', kwargs={'groupid': group.id}))

    return render(request, 'alert/enable_group_alert.html', {
        'form': form,
        'group': group
    })


def disable_group_alert(request, groupid):
    group = get_object_or_404(Group, id=groupid)
    alert = get_object_or_404(GroupAlert, group=group, user=request.user)
    form = DisableGroupAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the group %s' % group.name)
        return HttpResponseRedirect(reverse('group_details', kwargs={'groupid': group.id}))

    return render(request, 'alert/disable_group_alert.html', {
        'form': form,
        'group': group
    })


def alert_list_user(request):
    return alert_list(request, request.user)


def alert_list(request, user=None):
    sitealerts = SiteAlert.objects.filter(user=user if user else request.user)
    groupalerts = GroupAlert.objects.filter(user=user if user else request.user)
    tagalerts = TagAlert.objects.filter(user=user if user else request.user)

    return render(request, 'alert/alert_list.html', {
        'sitealerts': sitealerts,
        'groupalerts': groupalerts,
        'tagalerts': tagalerts,
        'filteruser': user
    })

