from .models import ApiClientState

def apiclientstate_processor(request):
    return {
        'apiclientstate': ApiClientState.objects.first()
    }

