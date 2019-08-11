from django.db import models
import json
from .message_generator import get_twilio_message


# Create your models here.
class Alarm(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    active = models.BooleanField()
    days_active = models.CharField(max_length=100)
    hour = models.IntegerField()
    minute = models.IntegerField()

    def set_days_active(self, days_active_str):
        self.days_active = json.dumps(days_active_str)

    def get_days_active(self):
        return json.loads(self.days_active)


class Global(models.Model):
    code = models.CharField(max_length=4, default='1234')
    alarm_ringing = models.BooleanField()
