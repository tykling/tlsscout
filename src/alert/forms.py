from django import forms
from django.conf import settings
from alert.models import SiteAlert, TagAlert, GroupAlert, AlertHistory

### enable site alert form
class EnableSiteAlertForm(forms.ModelForm):
    class Meta:
        model = SiteAlert
        fields = []

### disable site alert form
class DisableSiteAlertForm(forms.ModelForm):
    class Meta:
        model = SiteAlert
        fields = []

### enable group alert form
class EnableGroupAlertForm(forms.ModelForm):
    class Meta:
        model = GroupAlert
        fields = []

### disable group alert form
class DisableGroupAlertForm(forms.ModelForm):
    class Meta:
        model = GroupAlert
        fields = []

### enable tag alert form
class EnableTagAlertForm(forms.ModelForm):
    class Meta:
        model = TagAlert
        fields = []

### disable tag alert form
class DisableTagAlertForm(forms.ModelForm):
    class Meta:
        model = TagAlert
        fields = []

