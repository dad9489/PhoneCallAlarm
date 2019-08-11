from django import forms
from . import models


class CreateAlarm(forms.ModelForm):
    class Meta:
        model = models.Alarm
        fields = ['id', 'active', 'days_active', 'hour', 'minute']
