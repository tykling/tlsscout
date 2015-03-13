from django.conf import settings

def anon_access(request):
    return {
        'ALLOW_ANONYMOUS_VIEWING': settings.ALLOW_ANONYMOUS_VIEWING
    }

