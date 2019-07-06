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
        self.lights = self.hue.get_api()['lights']
        self.light_names = self.lights.keys()
        self.ringing = ringing

    def play(self):
        print('play begin')
        while True:
            pygame.mixer.init()

            stream = Stream(DOMAIN+'/public/alarm.mp3')
            pygame.mixer.music.load(stream)
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

        for light_name in self.light_names:
            self.hue.set_light(int(light_name), 'on', True)

        while self.ringing:
            for light_name in self.light_names:
                self.hue.set_light(int(light_name), 'xy', red)
                self.hue.set_light(int(light_name), 'bri', 255)
            sleep(sleep_time)
            for light_name in self.light_names:
                self.hue.set_light(int(light_name), 'xy', red)
                self.hue.set_light(int(light_name), 'bri', 0)
            sleep(sleep_time)
        for light_name in self.light_names:
            self.hue.set_light(int(light_name), 'xy', reading)
            self.hue.set_light(int(light_name), 'bri', 254)

    def ring(self):
        Thread(target=self.play).start()
        Thread(target=self.get_stop).start()
        Thread(target=self.blink_lights).start()
        while self.ringing:
            pass
        return True
