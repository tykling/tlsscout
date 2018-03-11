from django import forms
from group.models import Group
from django.conf import settings

### add/edit group form
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'interval_hours', 'publish', 'ignore_name_mismatch')

    def clean(self):
        ### get interval_hours from cleaned_data
        cleaned_data = super(GroupForm, self).clean()
        if 'interval_hours' in cleaned_data:
            interval_hours = cleaned_data.get("interval_hours")

            ### check if interval_hours is numeric
            try:
                temp = float(interval_hours)
            except:
                self._errors["interval_hours"] = self.error_class(["Invalid input"])
                del cleaned_data["interval_hours"]
                return cleaned_data
            
            ### check if interval_hours is lower than the limit
            if interval_hours < settings.MIN_CHECK_INTERVAL_HOURS:
                self._errors["interval_hours"] = self.error_class(["The lowest permitted check interval is %s hours" % settings.MIN_CHECK_INTERVAL_HOURS])
                del cleaned_data["interval_hours"]
                return cleaned_data
            
        ### return the cleaned data.
        return cleaned_data


### delete group form
class DeleteGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = []


### schedule urgent group check form
class ScheduleGroupCheckForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = []
