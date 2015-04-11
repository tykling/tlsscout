# tlsscout
tlsscout is a django implementation of the ssllabs website scanner API. 
You can run tlsscout on your own server to check your websites periodically, 
with alerting when something changes.

# Installation
See requirements.txt for a list of packages used by tlsscout. You will also need something
to serve the application. I prefer uwsgi behind an nginx server. YMMV.

Create a database, anything supported by Django is fine.

Copy settings.py.dist to settings.py and change:
- SECRET_KEY (make it a 100+ chars random string)
- ALLOWED_HOSTS (the domainname of your tlsscout instance)
- DATABASES section (database info and credentials)
- EMAIL_* (a valid mail account used for sending out emails)

Run "manage.py migrate" to populate the database, and then update 
the 'name' and 'domain' columns in the 'django_site' table to match
your tlsscout instance.

By default ALLOW_ANONYMOUS_VIEWING is True which means that the information
collected by the tlsscout instance is public without logging in. Set to false
to require login to see stuff.
