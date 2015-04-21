from eventlog.models import LogEntry

def AddLogEntry(username, type, event):
    logentry = LogEntry(username=username, type=type, event=event)
    logentry.save()
    return True
