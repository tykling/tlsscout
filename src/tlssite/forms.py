from tlssite.models import Site
from django import forms
import re
from taggit.forms import TagWidget


### add/edit site form
class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ('hostname','group', 'tags')
        widgets = {
            'tags': TagWidget(),
        }

    def clean(self):
        ### get cleaned_data
        cleaned_data = super(SiteForm, self).clean()
        hostname = cleaned_data.get("hostname")

        if hostname[0:8] == "https://":
            self._errors["hostname"] = self.error_class([u"please enter only hostnames, and remember only https on port 443 is supported"])
            del cleaned_data["hostname"]
            return cleaned_data

        if len(hostname) > 255:
            self._errors["hostname"] = self.error_class([u"valid hostnames are limited to 255 characters"])
            del cleaned_data["hostname"]
            return cleaned_data

        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(x) for x in hostname.split(".")):
            self._errors["hostname"] = self.error_class([u"invalid hostname"])
            del cleaned_data["hostname"]
            return cleaned_data

        ### return the cleaned data.
        return cleaned_data


### delete site form
class DeleteSiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = []

