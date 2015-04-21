"""
Django settings for tlsscout project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.conf import global_settings
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # allauth
    'allauth',
    'allauth.account',

    # pretty forms
    'bootstrapform',

    # tags
    'taggit',

    # tlsscout apps
    'dashboard',
    'tlssite',
    'group',
    'sitecheck',
    'ssllabs',
    'alert',
    'tag',
    'eventlog',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    # these three are required by allauth
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "tlsscout.template_context_processors.anon_access",
)

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'tlsscout.urls'
WSGI_APPLICATION = 'tlsscout.wsgi.application'

DEBUG = False
TEMPLATE_DEBUG = False

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# static files
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

# sites framework
SITE_ID = 1

# ssllabs API settings
SSLLABS_APIURL="https://api.ssllabs.com/api/v2/"
SSLLABS_TERMSURL="https://www.ssllabs.com/about/terms.html"
SSLLABS_SCANNERURL="https://www.ssllabs.com/ssltest/"
SSLLABS_POLITE_CONCURRENT_CHECKS = 1

# lower limit for the check interval
MIN_CHECK_INTERVAL_HOURS = 24

# allow anonymous / unauthenticated users to view data without logging in ?
ALLOW_ANONYMOUS_VIEWING = True

# allauth settings
# http://django-allauth.readthedocs.org/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION="mandatory"
ACCOUNT_AUTHENTICATION_METHOD="username_email"
ACCOUNT_EMAIL_REQUIRED=True
LOGIN_REDIRECT_URL = "/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from tlsscout_settings import *

# these depend on stuff defined in tlsscout_settings.py
DEFAULT_FROM_EMAIL=EMAIL_FROM
SERVER_EMAIL=EMAIL_FROM
if not ENABLE_SIGNUP:
    ACCOUNT_ADAPTER = 'tlsscout.adapters.SignupDisabledAdapter'

