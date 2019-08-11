from django.shortcuts import HttpResponse
from .models import Global


def code(request):
    global_obj = Global.objects.all()[0]
    return HttpResponse(global_obj.code)


def alarm_ringing(request):
    global_obj = Global.objects.all()[0]
    return HttpResponse(global_obj.alarm_ringing)
