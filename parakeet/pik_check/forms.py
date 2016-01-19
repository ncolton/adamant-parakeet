from __future__ import absolute_import

from django import forms
from . import models


class NewJobConfigurationForm(forms.Form):
    partner = forms.ModelChoiceField(
        queryset=models.Partner.objects.filter(jobconfiguration__isnull=True)
    )
    browsers = forms.ModelMultipleChoiceField(queryset=models.Browser.objects.all())
    enabled = forms.BooleanField()
    scheduling_interval = forms.DecimalField(min_value=0, decimal_places=0)
