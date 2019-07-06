"""
----- PROTOCOL/FLOW -----
Main runs, spawns two threads
    One thread waiting for time that alarm goes off checking alarm_times variable, runs forever
    One thread sending beats every 30 seconds, receives back alarm times and updates alarm_times variable, runs forever
When time, set flag for alarm, beat to alert website, call phone to start, start new threads
    One thread play sound, checking flag for code turned off, dies when turned off
    One thread waits a CALL_TIME amount of time, then if the alarm is still ringing, redials the phone,
        dies when alarm stops ringing
    One thread check website for flag turned off, then changes internal flag and dies
"""

import sys
import datetime
import requests
import time
from random import randint
from threading import Thread
from phone import begin_dial
from alarm import Alarm
from globals import DOMAIN

BEAT_TIME = 60      # the number of seconds to wait between beats
CALL_TIME = 120     # the number of seconds to wait between phone calls

alarm_ringing = False

day_to_number = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
number_to_day = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}


def beat():
    global wakeup_times
    data = {'device_name': 'Raspberry Pi', 'time': str(datetime.datetime.now()), 'alarm_bool': str(alarm_ringing)}
    r = requests.post(DOMAIN+'/beat', json=data)
    wakeup_times = r.json()
    print('beat response: '+str(r.text))


def beat_controller():
    while True:
        time.sleep(BEAT_TIME)
        if not alarm_ringing:
            beat()


def call_controller(code):
    while True:
        time.sleep(CALL_TIME)
        if alarm_ringing:
            print('trying call')
            begin_dial(code)
        else:
            break


def convert_days(days):
    """
    Converts array of weekdays as strings (eg. ["Monday", "Tuesday"]) to an array of ints (eg. [0, 1])
    :param days: array of weekdays as strings
    :return: an array of ints representing weekdays
    """
    days_as_num = []
    for day in days:
        days_as_num.append(day_to_number[day])
    return days_as_num


def time_checker():
    while True:
        try:
            now = datetime.datetime.now()
            for alarm in wakeup_times:
                alarm_hour, alarm_minute = str(alarm['hour']), str(alarm['minute'])
                today = datetime.datetime.today().weekday()  # number where 0 is Monday and 6 is Sunday
                if str(now.hour) == alarm_hour and str(now.minute) == alarm_minute and \
                        (today in convert_days(alarm['days_active'])) and alarm['active'] and not alarm_ringing:
                    Thread(target=ring_alarm).start()
                    time.sleep(60)
        except TypeError:
            pass


def ring_alarm():
    global alarm_ringing
    alarm_ringing = True
    beat()

    code = randint(1000, 9999)  # inclusive at both ends
    print('code: '+str(code))
    begin_dial(code)
    Thread(target=call_controller, args=(code,)).start()
    alarm = Alarm(alarm_ringing)
    alarm.ring()
    alarm_ringing = False


if __name__ == "__main__":

    wakeup_times = []

    # code for waiting. If debug, wait for input and start alarm. Else, spawn threads for time check and beat
    try:
        if sys.argv[1] == 'debug':
            input('Press enter to simulate alarm going off')
            print('ringing the alarm')
            ring_alarm()
        else:
            print('To debug, program argument should be exactly "debug". Otherwise, the program should be run with '
                  'no program arguments.')
            sys.exit()
    except IndexError:  # debug is not set in program arguments, real program is running
        # spawn time check and beat threads
        beat_thread = Thread(target=beat_controller).start()
        time_check_thread = Thread(target=time_checker).start()
