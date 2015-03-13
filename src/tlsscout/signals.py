from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from userprofile.models import UserProfile

### create profile on user creation
@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        profile = UserProfile(user=instance).save()
