from django.shortcuts import render, HttpResponse
from .models import Alarm
from . import forms
import json


# Create your views here.
def settings(request):
    if request.method == 'POST':
        print('****** caught POST ******')
        alarm_times = json.loads(request.POST['alarm_times'])
        for alarm in alarm_times:
            form = forms.CreateAlarm()
            try:
                instance = Alarm.objects.get(id=alarm['id'])
                x = 1
            except Alarm.DoesNotExist:
                instance = form.save(commit=False)
                instance.id = alarm['id']
            instance.active = alarm['active']
            instance.days_active = json.dumps(alarm['days_active'])
            instance.hour = alarm['hour']
            instance.minute = alarm['minute']
            instance.save()

        return HttpResponse(request)
    else:
        form = forms.CreateAlarm()
        alarms = Alarm.objects.all()
        return render(request, 'settings/settings.html', {'alarms': alarms, 'form': form})
