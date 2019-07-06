from phue import Bridge
from time import sleep


hue = Bridge('192.168.1.39')

hue.connect()

lights = hue.get_api()['lights']

light_names = lights.keys()

red = [0.6786, 0.3159]
reading = [0.4452, 0.4068]
sleep_time = 0.5

while True:
    for light_name in light_names:
        hue.set_light(int(light_name), 'xy', red)
        hue.set_light(int(light_name), 'bri', 255)
    sleep(sleep_time)
    for light_name in light_names:
        hue.set_light(int(light_name), 'xy', red)
        hue.set_light(int(light_name), 'bri', 0)
    sleep(sleep_time)


for light_name in light_names:
    hue.set_light(int(light_name), 'xy', reading)
    hue.set_light(int(light_name), 'bri', 254)
