from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

def send_email(subject, from_email, recipient, text_content, html_content):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
def tlsscout_alert(oldcheck, newcheck):
    ### get hostname for this tlsscout instance (for use in the email)
    current_site = Site.objects.get_current()
    
    ### start putting the email together
    from_email = "%s <%s>" % (current_site.domain, settings.EMAIL_FROM)
    try:
        subject = "tlsscout alert: Rating for site %s changed!" % oldcheck.site.hostname
        formatdict={
            'oldresultstring': "/".join([result.grade for result in oldcheck.results.all()]) if oldcheck.results.all() else None,
            'newresultstring': "/".join([result.grade for result in newcheck.results.all()]) if newcheck.results.all() else None,
            'site': oldcheck.site,
            'baseurl': 'https://%s' % current_site.domain,
        }
        text_content = render_to_string('emails/result_changed.txt', formatdict)
        html_content = render_to_string('emails/result_changed.html', formatdict)
        
        ### find out who should receive this alert
        for recipient in oldcheck.site.get_alert_users().all():
            send_email(subject, from_email, recipient.email, text_content, html_content)
    except Exception as E:
        print "exception while rendering and sending email: %s" % E
        return False

