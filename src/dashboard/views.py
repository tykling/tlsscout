from django.shortcuts import render
from django.conf import settings

def dashboard(request):
    if request.user.is_authenticated:
        ### show dashboard
        return render(request, 'dashboard.html')
    else:
        ### show frontpage with brief teaser and login box
        return render(request, 'frontpage.html', {
            'SSLLABS_SCANNERURL': settings.SSLLABS_SCANNERURL,
            'SSLLABS_TERMSURL': settings.SSLLABS_TERMSURL,
            'ENABLE_SIGNUP': settings.ENABLE_SIGNUP,
        })

