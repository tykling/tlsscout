# local settings for this tlsscout installation,
# the {{ foo }} bits should be replaced with real values (by Ansible or by hand)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hemmelig'

# debug settings - remember to set allowed_hosts if debug is disabled
DEBUG=True
ALLOWED_HOSTS = []

# Database settings
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tlsscoutdb',
        'USER': 'tlsscout',
        'PASSWORD': 'tlsscout',
        'HOST': '127.0.0.1',
    },
}

# admin site url prefix, set to 'admin' for /admin/
ADMIN_PREFIX='admin'

# email settings
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
#EMAIL_HOST='mailhost.example.com'
#EMAIL_PORT=587
#EMAIL_HOST_USER='mymailuser'
#EMAIL_HOST_PASSWORD='mymailpassword'
#EMAIL_USE_TLS=True
#EMAIL_FROM='noreply@example.com'     # NOTE: this email is included in the useragent when using the SSL Labs API

# enable new accout creation / signups / registration?
ENABLE_SIGNUP=True

# pagination
EVENTS_PER_PAGE=100

