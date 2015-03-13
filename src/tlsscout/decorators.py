from django.conf import settings

### used by @user_passes_test decorator on readonly views
def logged_in_or_anon_allowed(user):
    if user.is_authenticated() or settings.ALLOW_ANONYMOUS_VIEWING:
        return True
    else:
        return False

