import pygame
from threading import Thread
import requests
import urllib.request
import time
from globals import DOMAIN
from globals import Stream

class Alarm:
    def __init__(self, ringing):
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

    def ring(self):
        sound_thread = Thread(target=self.play).start()
        stop_thread = Thread(target=self.get_stop).start()
        while self.ringing:
            pass
        return True
