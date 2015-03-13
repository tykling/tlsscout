from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from userprofile.models import UserProfile
from userprofile.forms import ProfileForm

### show profile
@login_required
def profile_show(request):
    ### get user profile
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'userprofile/profile_show.html')


### edit profile function
@login_required
def profile_edit(request):
    ### get the profile
    profile = get_object_or_404(UserProfile, user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)

    ### check if the form has been POSTed and is valid
    print "checking form.."
    if form.is_valid():
        print "form is valid"
        profile = form.save()
        print profile.last_name
        return HttpResponseRedirect(reverse('profile_show'))
    else:
        print "form not valid"

    ### return response
    return render(request, 'userprofile/profile_edit.html', {
        'form': form
    })
