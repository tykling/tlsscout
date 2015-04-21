from ssllabs.api import Info, Analyze
from ssllabs.models import ApiClientState
from sitecheck.models import SiteCheck
from django.utils import timezone
from django.conf import settings
from eventlog.utils import AddLogEntry
import json


def StartScan(sitecheck):
    ### check how many assessments are currently running from this IP,
    ### may include more than just our own assessments
    infojson = Info()
    if infojson['currentAssessments'] == infojson['maxAssessments']:
        #print "can't start any more new assessments at this time, urgent or not"
        return False
    
    ### get apiclientstate from DB
    apiclientstate = ApiClientState.objects.get(id=1)

    ### check how many assessments this tlsscout instance is running in total
    ourass = SiteCheck.objects.filter(start_time__isnull=False, finish_time__isnull=True)
    if ourass:
        if ourass.count() >= apiclientstate.max_concurrent_assessments:
            #print "can't start any more new assessments at this time, urgent or not"
            return False

        ### check how many of the running assessments are not urgent
        if ourass.filter(urgent=False).count() >= settings.SSLLABS_POLITE_CONCURRENT_CHECKS:
            #print "can't start any more assessments unless they are urgent"
            urgentonly=True
        else:
            #print "new assessments can be started"
            urgentonly=False
    else:
        #print "new assessments can be started"
        urgentonly=False

    ### can this sitecheck be started?
    if sitecheck.urgent or not urgentonly:
        if sitecheck.urgent:
            AddLogEntry(username='tlsscout engine', type='engine', event='starting urgent check of site %s' % sitecheck.site.hostname)
        else:
            AddLogEntry(username='tlsscout engine', type='engine', event='starting regular scheduled check of site %s' % sitecheck.site.hostname)

        ### make an API call to start the check
        hostinfo = Analyze(
            host=sitecheck.site.hostname, 
            startNew="on", 
            publish="on" if sitecheck.site.group.publish else "off", 
            ignorename="on" if sitecheck.site.group.ignore_name_mismatch else "off",
            all="done", 
            sitecheck=sitecheck
        )
        sitecheck.start_time=timezone.now()
        sitecheck.json_result=json.dumps(hostinfo)
        if 'status' in hostinfo:
            if 'statusMessage' in hostinfo:
                sitecheck.status_message = "%s: %s" % (hostinfo['status'], hostinfo['statusMessage'])
            else:
                sitecheck.status_message = hostinfo['status']
        else:
                sitecheck.status_message = "unknown (API didn't supply a status message)"
        sitecheck.save()


def GetResults(sitecheck):
    hostinfo = Analyze(
        host=sitecheck.site.hostname, 
        publish="on" if sitecheck.site.group.publish else "off",
        ignorename="on" if sitecheck.site.group.ignore_name_mismatch else "off",
        all="done", 
        sitecheck=sitecheck
    )
    return hostinfo

