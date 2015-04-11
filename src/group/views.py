from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from group.models import Group
from group.forms import GroupForm, DeleteGroupForm, ScheduleGroupCheckForm
from tlssite.models import Site
from django.core.urlresolvers import reverse, reverse_lazy
from sitecheck.models import SiteCheck, SiteCheckResult
from django.conf import settings
from tlsscout.decorators import logged_in_or_anon_allowed
from django.contrib import messages
from tlssite.views import start_urgent_check_ok


### add/edit group function
@login_required
def group_add_edit(request,groupid=None):
    if groupid:
        group = get_object_or_404(Group, id=groupid)
        form = GroupForm(request.POST or None, instance=group)
        template = 'group_edit.html'
    else:
        form = GroupForm(request.POST or None)
        template = 'group_add.html'

    if form.is_valid():
        group = form.save()
        if groupid:
            messages.success(request, 'The group "%s" has been updated.' % group.name)
        else:
            messages.success(request, 'The group "%s" has been created.' % group.name)
        return HttpResponseRedirect(reverse('group_list'))

    return render(request, template, {
        'form': form
    })


### delete group
@login_required
def group_delete(request, groupid):
    ### if this group doesn't exist return 404
    group = get_object_or_404(Group, id=groupid)

    if group.sites.count() > 0:
        return render(request, 'group_delete_fail.html', {
            'group': group
        })
    
    form = DeleteGroupForm(request.POST or None, instance=group)
    if form.is_valid():
        group.delete()
        messages.success(request, 'The group "%s" has been deleted.' % group.name)
        return HttpResponseRedirect(reverse('group_list'))

    return render(request, 'group_delete_confirm.html', {
        'group': group,
        'form': form
    })


### list groups
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def group_list(request):
    ### get a list of groups
    groups = Group.objects.all()

    return render(request, 'group_list.html', {
        'groups': groups,
    })


### show group details
@user_passes_test(logged_in_or_anon_allowed, login_url=reverse_lazy('account_login'))
def group_details(request,groupid):
    ### if this group doesn't exist return 404
    group = get_object_or_404(Group, id=groupid)    
    return render(request, 'group_details.html', {
        'group': group
    })


### urgent group check
@login_required
def group_check(request, groupid):
    group = get_object_or_404(Group, id=groupid)
    form = ScheduleGroupCheckForm(request.POST or None, instance=group)
    if form.is_valid():
        sites = Site.objects.filter(group=group)
        checkcounter = 0
        for site in sites:
            if not start_urgent_check_ok(site):
                messages.error(request, 'A check of the site "%s" is already running, or an urgent check is already scheduled. Not scheduling a new urgent check.' % site.hostname)
            else:
                check = SiteCheck(site=site, urgent=True)
                check.save()
                checkcounter += 1
        if checkcounter > 0:
            messages.success(request, 'Scheduled an urgent check for %s sites in the group "%s"' % (checkcounter, group.name))
        else:
            messages.error(request, 'No new urgent checks scheduled!')
        return HttpResponseRedirect(reverse('group_details', kwargs={'groupid': groupid}))

    return render(request, 'group_check_confirm.html', {
        'group': group,
        'form': form
    })
