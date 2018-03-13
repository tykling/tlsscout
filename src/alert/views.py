from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from tlssite.models import Site
from group.models import Group
from alert.models import SiteAlert, TagAlert, GroupAlert
from alert.forms import EnableSiteAlertForm, DisableSiteAlertForm, EnableGroupAlertForm, DisableGroupAlertForm, EnableTagAlertForm, DisableTagAlertForm
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from eventlog.utils import AddLogEntry

@login_required
def enable_site_alert(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    form = EnableSiteAlertForm(request.POST or None)

    # check if alerting is already enabled for this site
    try:
        alert = SiteAlert.objects.get(user=request.user, site=site)
        messages.error(request, 'Alerting is already enabled for the site "%s"' % site.hostname)
    except SiteAlert.DoesNotExist:
        if form.is_valid():
            alert = SiteAlert.objects.create(user=request.user, site=site)
            messages.success(request, 'Alerting has now been enabled for the site "%s"' % site.hostname)
            AddLogEntry(username=request.user, type='configchange', event='Enabled alerting for the user %s for the site %s' % (alert.user, site.hostname))
            return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': site.id}))

    return render(request, 'enable_site_alert.html', {
        'form': form,
        'site': site
    })


@login_required
def disable_site_alert(request, siteid):
    site = get_object_or_404(Site, id=siteid)
    alert = SiteAlert.objects.get(user=request.user, site=site)
    form = DisableSiteAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the site "%s" for user "%s"' % (alert.site.hostname, alert.user))
        AddLogEntry(username=request.user, type='configchange', event='Disabled alerting for the user "%s" for the site "%s"' % (alert.user, alert.site.hostname))
        return HttpResponseRedirect(reverse('site_details', kwargs={'siteid': alert.site.id}))

    return render(request, 'disable_site_alert.html', {
        'form': form,
        'site': alert.site,
        'user': alert.user
    })


@login_required
def enable_tag_alert(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    alert = TagAlert.objects.get(user=request.user, tag=tag)
    form = EnableTagAlertForm(request.POST or None)

    # check if alerting is already enabled for this tag
    try:
        messages.error(request, 'Alerting is already enabled for the tag "%s"' % tag)
    except TagAlert.DoesNotExist:
        if form.is_valid():
            alert = TagAlert.objects.create(user=request.user, tag=tag)
            messages.success(request, 'Alerting has now been enabled for the tag "%s"' % tag)
            AddLogEntry(username=request.user, type='configchange', event='Enabled alerting for the user "%s" for the tag "%s"' % (alert.user, tag))
            return HttpResponseRedirect(reverse('tag_list'))

    return render(request, 'enable_tag_alert.html', {
        'form': form,
        'tag': tag
    })


@login_required
def disable_tag_alert(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    alert = TagAlert.objects.get(user=request.user, tag=tag)
    form = DisableTagAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the tag "%s" for the user "%s"' % (alert.tag, alert.user))
        AddLogEntry(username=request.user, type='configchange', event='Disabled alerting for the user "%s" for the tag "%s"' % (alert.user, alert.tag))
        return HttpResponseRedirect(reverse('tag_list'))

    return render(request, 'disable_tag_alert.html', {
        'form': form,
        'tag': alert.tag,
        'user': alert.user
    })


@login_required
def enable_group_alert(request, groupid):
    group = get_object_or_404(Group, id=groupid)
    form = EnableGroupAlertForm(request.POST or None)

    # check if alerting is already enabled for this group
    try:
        alert = GroupAlert.objects.get(user=request.user, group=group)
        messages.error(request, 'Alerting is already enabled for the group "%s"' % group.name)
    except GroupAlert.DoesNotExist:
        if form.is_valid():
            alert = GroupAlert.objects.create(user=request.user, group=group)
            messages.success(request, 'Alerting has now been enabled for the group "%s"' % group.name)
            AddLogEntry(username=request.user, type='configchange', event='Enabled alerting for the user "%s" for the group "%s"' % (alert.user, group.name))
            return HttpResponseRedirect(reverse('group_details', kwargs={'groupid': group.id}))

    return render(request, 'enable_group_alert.html', {
        'form': form,
        'group': group
    })


@login_required
def disable_group_alert(request, groupid):
    group = get_object_or_404(Group, id=groupid)
    alert = GroupAlert.objects.get(user=request.user, group=group)
    form = DisableGroupAlertForm(request.POST or None, instance=alert)

    if form.is_valid():
        alert.delete()
        messages.success(request, 'Alerting has been disabled for the group "%s" for the user "%s"' % (alert.group.name, alert.user))
        AddLogEntry(username=request.user, type='configchange', event='Disabled alerting for the user "%s" for the group "%s"' % (alert.user, alert.group.name))
        return HttpResponseRedirect(reverse('group_list'))

    return render(request, 'disable_group_alert.html', {
        'form': form,
        'group': alert.group,
        'user': alert.user
    })


@login_required
def alert_list_user(request):
    return alert_list(request, request.user)


@login_required
def alert_list(request, user=None):
    if user:
        sitealerts = SiteAlert.objects.filter(user=user)
        groupalerts = GroupAlert.objects.filter(user=user)
        tagalerts = TagAlert.objects.filter(user=user)
    else:
        sitealerts = SiteAlert.objects.all()
        groupalerts = GroupAlert.objects.all()
        tagalerts = TagAlert.objects.all()

    return render(request, 'alert_list.html', {
        'sitealerts': sitealerts,
        'groupalerts': groupalerts,
        'tagalerts': tagalerts,
        'filteruser': user
    })

