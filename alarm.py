import pygame
from threading import Thread
import requests
from time import sleep
from globals import DOMAIN
from globals import Stream
from phue import Bridge


class Alarm:
    def __init__(self, ringing):
        self.hue = Bridge('192.168.1.39')
        self.hue.connect()
        self.light_group = int(list(self.hue.get_api()['groups'].keys())[0])
        # self.light_names = self.lights.keys()
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
        red = [0.6786, 0.3159]
        reading = [0.4452, 0.4068]
        sleep_time = 0.5

        self.hue.set_group(self.light_group, 'on', True)
        self.hue.set_group(self.light_group, 'xy', red)

        while self.ringing:
            self.hue.set_group(self.light_group, 'bri', 255)
            sleep(sleep_time)
            self.hue.set_group(self.light_group, 'bri', 0)
            sleep(sleep_time)
        self.hue.set_group(self.light_group, 'xy', reading)
        self.hue.set_group(self.light_group, 'bri', 254)

    def ring(self):
        Thread(target=self.play).start()
        Thread(target=self.get_stop).start()
        Thread(target=self.blink_lights).start()
        while self.ringing:
            pass
        return True
