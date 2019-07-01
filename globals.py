DOMAIN = 'https://phone-call-alarm.appspot.com'

import requests


# File like object that streams the object from URL
class Stream(object):

    def __init__(self, url):
        self._file = requests.get(url, stream=True)

    def read(self, *args):
        if args:
            return self._file.raw.read(args[0])
        else:
            return self.file.raw.read()

    def close(self):
        self._file.close()
