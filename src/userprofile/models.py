from django.db import models
from django.contrib.auth.models import User

### model for user profiles
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)

