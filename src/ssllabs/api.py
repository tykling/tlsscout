from django.conf import settings
from django.utils import timezone
from ssllabs.models import ApiClientState, RequestLog
import requests, json, uuid
from random import randint

# SSL Labs API documentation: 
# https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md

def __MakeRequest(url, payload=None, sitecheck=None):
    requestuuid = str(uuid.uuid4())
    ua = 'tlsscout request %s (%s)' % (requestuuid, requests.utils.default_user_agent())
    headers = {
        'User-Agent': ua,
        'From': settings.DEFAULT_FROM_EMAIL
    }
    r = requests.get(url, params=payload, headers=headers)
    __SaveRequest(request=r, sitecheck=sitecheck, uuid=requestuuid)
    return r


def __InitApiClient():
    ### Make an info call to get X-Max-Assessments and X-Current-Assessments
    r = __MakeRequest(settings.SSLLABS_APIURL + 'info')

    if not 'X-Max-Assessments' in r.headers:
        print("X-Max-Assessments missing from API response. Bailing out.")
        return False

    if not 'X-Current-Assessments' in r.headers:
        print("X-Current-Assessments missing from API response. Bailing out.")
        return False

    maxass = int(r.headers['X-Max-Assessments'])
    curass = int(r.headers['X-Current-Assessments'])
    if curass > 0:
        ### one or more assessments are already running,
        ### it appears we are not the only SSL Labs API client on this IP.
        ### divide the permitted max. number of concurrent assessments by two
        maxass = maxass / 2

    apiclientstate = ApiClientState(max_concurrent_assessments=maxass)
    apiclientstate.save()
    return apiclientstate


def __ApiCall(method, payload=None, sitecheck=None):
    ### get (or create) apiclientstate from DB
    try:
        apiclientstate = ApiClientState.objects.get(id=1)
    except ApiClientState.DoesNotExist:
        ### first API run. 
        apiclientstate = __InitApiClient()
        if not apiclientstate:
            print("something went wrong while initializing the API client")
            return False

    ### find out if we are supposed to be sleeping
    if apiclientstate.sleep_until:
        if apiclientstate.sleep_until > timezone.now():
            print("API client should sleep until %s" % apiclientstate.sleep_until)
            return False
        else:
            ### done sleeping
            apiclientstate.sleep_until = None
            apiclientstate.save()

    ### make an ssllabs API call
    r = __MakeRequest(settings.SSLLABS_APIURL + method, payload=payload, sitecheck=sitecheck)

    ### check the response status code here
    if r.status_code == 400:
        print("API returned HTTP 400: invocation error (e.g., invalid parameters)")
        return False

    if r.status_code == 429:
        ### too many concurrent assessments from this IP
        print("API returned HTTP 429: client request rate too high")

        ### perhaps more than one SSL Labs API client are running from this ip?
        ### divide the current max_concurrent_assessments by two to accomodate
        apiclientstate.max_concurrent_assessments=apiclientstate.max_concurrent_assessments/2
        apiclientstate.sleep_until = timezone.now() + timedelta(minutes=5)
        apiclientstate.save()
        return False

    if r.status_code == 500:
        ### internal server error on the API server
        print("API returned HTTP 500: internal error")
        return False

    if r.status_code == 503:
        ### maintenance
        print("API returned HTTP 503: the service is not available (e.g., down for maintenance)")
        apiclientstate.sleep_until = timezone.now() + timedelta(minutes=15)
        apiclientstate.save()
        return False

    if r.status_code == 529:
        ### API service overloaded
        print("API returned HTTP 529: the service is overloaded")

        ### API docs says to "randomize backoff time" on HTTP 529, so sleep between 30 and 60 minutes
        apiclientstate.sleep_until = timezone.now() + timedelta(minutes=randint(30,60))
        apiclientstate.save()
        return False

    ### return the result
    return r.json()


def __SaveRequest(request, sitecheck, uuid):
    requestlog = RequestLog(
        sitecheck=sitecheck,
        request_url=request.url,
        request_headers=json.dumps(dict(request.request.headers)),
        response_code=request.status_code,
        response_headers=json.dumps(dict(request.headers)),
        response_body=request.text,
        uuid=uuid
    )
    requestlog.save()


def Info():
    infojson = __ApiCall("info")
    return infojson


def Analyze(host, publish=None, ignorename=None, startNew=None, fromCache=None, maxAge=None, all=None, sitecheck=None):
    ### start putting params together, host is required
    params = {'host': host}

    ### publish parameter, should be "on" or "off", API defaults to off
    if publish:
        if publish != "on" and publish != "off":
            # invalid option
            print("invalid publish option")
            return False
        else:
            params['publish'] = publish

    ### ignorename parameter, should be "on" or "off"
    if ignorename:
        if ignorename != "on" and ignorename != "off":
            # invalid option
            print("invalid ignorename option")
            return False
        else:
            params['ignoreMismatch'] = ignorename

    ### startNew parameter, only valid value is "on"
    if startNew:
        if startNew != "on":
            print("invalid startNew value")
            return False
        else:
            params['startNew'] = startNew

    ### fromCache parameter, can be "on" or "off" and can't be used with startNew, API defaults to off
    if fromCache:
        if fromCache != "on" and fromCache != "off":
            # invalid option
            print("invalid fromCache parameter")
            return False
        else:
            if startNew:
                # invalid
                print("fromCache can't be used with startNew")
                return False
            params['fromCache'] = fromCache

    ### maxAge parameter, maximum report age, in hours, if retrieving from cache (fromCache parameter set).
    if maxAge:
        if not fromCache or fromCache=="off":
            # invalid option
            print("maxAge only makes sense when fromCache is on")
            return False
        else:
            params['maxAge'] = maxAge

    ### all parameter, valid values "on" or "done"
    if all:
        if all != "on" and all != "done":
            # invalid option
            print("invalid all option")
            return False
        else:
            params['all'] = all


    ### make request
    hostinfo = __ApiCall(method="analyze", payload=params, sitecheck=sitecheck) 
    return hostinfo


def GetEndpointData(host, s, fromCache):
    ### start putting params together, host and s is required
    params = {'host': host}
    params = {'s': s}

    ### fromCache parameter, can be "on" or "off", API defaults to off
    if fromCache:
        if fromCache != "on" and fromCache != "off":
            # invalid option
            print("invalid fromCache parameter")
            return False
        else:
            params['fromCache'] = fromCache

    ### maxAge parameter
    endpointinfo = __ApiCall("analyze", params) 
    return endpointinfo


def GetStatusCodes():
    status_codes = __ApiCall("getStatusCodes")
    return status_codes

