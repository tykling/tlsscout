from django import forms
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

### add/edit profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name')

