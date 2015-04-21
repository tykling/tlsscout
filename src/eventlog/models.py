from django.db import models

class LogEntry(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    event = models.TextField()

