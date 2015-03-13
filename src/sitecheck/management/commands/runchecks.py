from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from sitecheck.models import SiteCheck, SiteCheckResult
from ssllabs.wrappers import StartScan, GetResults
from tlssite.models import Site
import os, socket, sys, datetime, atexit, json
import tempfile

class Command(BaseCommand):
    args = 'none'
    help = 'Run checks when needed'

    ### called by django when the management command is run
    def handle(self, *args, **options):
        pid = str(os.getpid())
        pidfile = os.path.join(tempfile.gettempdir(),"tlsscout-engine.pid")
        
        if os.path.isfile(pidfile):
            self.stdout.write("%s already exists, exiting" % pidfile)
            sys.exit()
        else:
            self.stdout.write("writing pidfile")
            file(pidfile, 'w').write(pid)
            atexit.register(self.__RmPidFile, pidfile)
    
        ### update the status of running checks first, to see if anything finished
        self.stdout.write("- update status of running checks...")
        self.__UpdateRunningChecks()


        ### see if any new urgent checks need to be started
        self.stdout.write("- starting urgent checks...")
        self.__StartUrgentChecks()


        ### see if any regular new checks need to be started
        self.stdout.write("- starting regular checks...")
        self.__StartRegularChecks()


    ### clean up method
    def __RmPidFile(self, pidfile):
        self.stdout.write("deleting pidfile")
        os.unlink(pidfile)


    ### method to start urgent checks
    def __StartUrgentChecks(self):
        urgentchecks = SiteCheck.objects.filter(urgent=True, start_time__isnull=True, finish_time__isnull=True)
        for check in urgentchecks:
            self.stdout.write("starting urgent check of site %s" % check.site.hostname)
            StartScan(check)


    ### method to start regular checks
    def __StartRegularChecks(self):
        sites = Site.objects.all()
        for site in sites:
            ### if this site has no checks at all start one now
            if SiteCheck.objects.filter(site=site).count() == 0:
                ### start a new check
                self.stdout.write("starting new check of site %s" % site.hostname)
                check = SiteCheck(site=site)
                check.save()
                StartScan(check)
                continue

            ### this site has one or more checks in database, see is any are started but not finished
            checks = SiteCheck.objects.filter(site=site, start_time__isnull=False, finish_time__isnull=True)
            if checks:
                self.stdout.write("found a running check for site %s, not starting a new one" % site.hostname)
                continue
            
            ### this site has no currently running checks, see if one was added but never started
            ### (only one such check should ever exist)
            try:
                check = SiteCheck.objects.get(site=site, start_time__isnull=True, finish_time__isnull=True)
                self.stdout.write("found unstarted check for site %s, starting it..." % site.hostname)
                StartScan(check)
                continue
            except SiteCheck.DoesNotExist:
                pass

            ### all checks for this site are finished, find the finish time of the latest completed check
            latestcheck = SiteCheck.objects.filter(site=site).latest('finish_time')
            if latestcheck.finish_time + timedelta(hours=site.group.interval_hours) > timezone.now():
                ### not yet
                continue
            else:
                ### it is time to run a new check of this site
                self.stdout.write("it is time for a new check of site %s, starting " % site.hostname)
                check = SiteCheck(site=site)
                check.save()
                StartScan(check)


    ### method to update the status of running checks
    def __UpdateRunningChecks(self):
        runningchecks = SiteCheck.objects.filter(start_time__isnull=False, finish_time__isnull=True)

        ### loop through them and check each to see if it is finished yet
        for check in runningchecks:
            self.stdout.write("checking status of running check for site %s" % check.site.hostname)
            ### make an API call to see if the check has finished
            hostinfo = GetResults(check)
            if not hostinfo:
                ### something went wrong while running the check, error
                check.status = "APIERROR"
                check.status_message = "Something went wrong while running the check"
                check.finish_time=timezone.now()
            elif 'status' not in hostinfo:
                ### hostinfo does not contain a status field, error
                check.status = "APIERROR"
                check.status_message = "No 'status' value was received from the SSL Labs API"
                check.finish_time=timezone.now()
            elif hostinfo['status'] == "DNS":
                ### check is in status DNS
                check.status = "DNS"
                check.status_message = None
            elif hostinfo['status'] == "ERROR":
                ### check has failed with an error
                check.status = "ERROR"
                check.status_message = None
                check.finish_time=timezone.now()
            elif hostinfo['status'] == "IN_PROGRESS":
                ### check is still running, patience pls
                check.status = "IN_PROGRESS"
                check.status_message = None
                check.json_result = json.dumps(hostinfo)
                check.save()
                self.__ParseResultJson(sitecheck=check, hostinfo=hostinfo)
                self.stdout.write("check of site %s is still running.." % check.site.hostname)
            elif hostinfo['status'] == "READY":
                ### check is finished, yay
                check.status = "READY"
                check.status_message = None
                check.json_result = json.dumps(hostinfo)
                check.finish_time=timezone.now()
                check.save()
                self.__ParseResultJson(sitecheck=check, hostinfo=hostinfo)
                self.stdout.write("check of site %s is finished!" % check.site.hostname)
            else:
                ### hostinfo field has an unknown value, error
                check.status = "APIERROR"
                check.status_message = "An unexpected 'status' value was received from the SSL Labs API"
                check.finish_time=timezone.now()

            ### save the check and continue
            check.save()
            self.stdout.write("finished updating check of site %s" % check.site.hostname)
            continue


    ### method to parse result json
    def __ParseResultJson(self, sitecheck, hostinfo):
        # parse result dict into SiteCheckResult model
        for endpoint in hostinfo['endpoints']:
            ### check if this endpoint exists in DB
            try:
                result = SiteCheckResult.objects.get(sitecheck=sitecheck, serverip=endpoint['ipAddress'])
            except SiteCheckResult.DoesNotExist:            
                result = SiteCheckResult(
                    sitecheck = sitecheck,
                    serverip = endpoint['ipAddress']
                )
            if 'serverName' in endpoint:
                result.serverhostname = endpoint['serverName']

            if 'grade' in endpoint:
                result.grade = endpoint['grade']
            else:
                result.grade = None

            if 'statusMessage' in endpoint:
                result.status_message = endpoint['statusMessage']
            else:
                result.status_message = None

            if 'statusDetailsMessage' in endpoint:
                result.status_details_message = endpoint['statusDetailsMessage']
            else:
                result.status_details_message = None

            ### save 
            result.save()

