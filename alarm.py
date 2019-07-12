import pygame
from threading import Thread
import requests
from time import sleep
from globals import DOMAIN
from globals import Stream
from phue import Bridge
from phue import PhueRegistrationException


class Alarm:
    def __init__(self, ringing):
        self.ringing = ringing

    def play(self):
        print('play begin')
        while True:
            pygame.mixer.init()

            # stream = Stream(DOMAIN+'/public/alarm.mp3')
            # pygame.mixer.music.load(stream)
            pygame.mixer.music.load('./php/public/alarm.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.ringing:
                continue
            if not self.ringing:
                break
        pygame.mixer.quit()
        print('play stopped')

    def get_stop(self):
        while self.ringing:
            r = requests.get(url=DOMAIN+'/alarm_bool')
            self.ringing = (r.text == 'True')

    def blink_lights(self):
        try:
            ip = requests.get('https://www.meethue.com/api/nupnp').json()[0]['internalipaddress']
            hue = Bridge(ip)
            hue.connect()
            light_group = int(list(hue.get_api()['groups'].keys())[0])
            red = [0.6786, 0.3159]
            reading = [0.4452, 0.4068]
            sleep_time = 0.5

            # save the original light settings, so they can be reset when the alarm is turned off
            lights = hue.get_api()['lights']
            orig_settings = {}
            for light_id in lights.keys():
                light = lights[light_id]
                xy = light['state']['xy']
                bri = light['state']['bri']
                on = light['state']['on']
                orig_settings[light_id] = xy, bri, on
            print(orig_settings)

            hue.set_group(light_group, 'on', True)
            hue.set_group(light_group, 'xy', red)

            while self.ringing:
                hue.set_group(light_group, 'bri', 255)
                sleep(sleep_time)
                hue.set_group(light_group, 'bri', 0)
                sleep(sleep_time)

            # return the lights to their original settings
            for light_id in orig_settings.keys():
                orig_setting = orig_settings[light_id]
                command = {'xy': orig_setting[0], 'bri': orig_setting[1], 'on': orig_setting[2]}
                hue.set_light(int(light_id), command)
        except PhueRegistrationException:
            print('ERROR: The link button needs to be pressed to control the lights')

    def ring(self):
        Thread(target=self.play).start()
        Thread(target=self.get_stop).start()
        Thread(target=self.blink_lights).start()
        while self.ringing:
            pass
        return True
