"""
Django settings for tlsscout project.
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from .environment_settings import *

INSTALLED_APPS = [
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
    'allauth.socialaccount',

    # pretty forms
    'bootstrapform',

    # tags
    'taggit',

    # channels
    'channels',

    # tlsscout apps
    'dashboard',
    'tlssite',
    'group',
    'sitecheck',
    'ssllabs',
    'alert',
    'tag',
    'eventlog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

ROOT_URLCONF = 'tlsscout.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ssllabs.context_processors.apiclientstate_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'tlsscout.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_src')]

ASGI_APPLICATION = "tlsscout.routing.application"

# sites framework required for allauth
SITE_ID = 1

# allauth settings
# http://django-allauth.readthedocs.org/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION="mandatory"
ACCOUNT_AUTHENTICATION_METHOD="username_email"
ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
LOGIN_REDIRECT_URL = "/"

# ssllabs API settings
SSLLABS_APIURL="https://api.ssllabs.com/api/v2/"
SSLLABS_TERMSURL="https://www.ssllabs.com/about/terms.html"
SSLLABS_SCANNERURL="https://www.ssllabs.com/ssltest/"
SSLLABS_POLITE_CONCURRENT_CHECKS = 1

# lower limit for the check interval
MIN_CHECK_INTERVAL_HOURS = 24

# allow anonymous / unauthenticated users to view data without logging in ?
ALLOW_ANONYMOUS_VIEWING = True

# disable signups in allauth as needed
if not ENABLE_SIGNUP:
  ACCOUNT_ADAPTER = 'tlsscout.adapters.SignupDisabledAdapter'

