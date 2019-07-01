from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import requests
from globals import DOMAIN

TWILIO_PHONE_NUMBER = "+13103214853"

# list of one or more phone numbers to dial, in "+19732644210" format
DIAL_NUMBERS = ["+18645207019", ]

# replace the placeholder values with your Account SID and Auth Token
# found on the Twilio Console: https://www.twilio.com/console
client = Client("ACf43effe9a0a3ed1719c809e7f6f736f9", "d3bcfa3769088d3435c984926d8411d2")


def begin_dial(code):
    if post_message(str(code), create_message(str(code))):
        dial_numbers(DIAL_NUMBERS)
        # print(create_message(code))
        print('success')
    else:
        print('An error occurred while uploading the message.')


def create_message(code):
    number_map = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
                  '8': 'eight', '9': 'nine', '0': 'zero'}
    code_str = ''
    for digit in str(code):
        code_str = code_str + ' ' + number_map[digit]
    return "Good morning! To turn off the alarm, enter code" + code_str + ". Again, that's code" + code_str + \
           ". One more time, code" + code_str + ". Have a great day!"


def dial_numbers(numbers_list):
    """Dials one or more phone numbers from a Twilio phone number."""
    for number in numbers_list:
        print("Dialing " + number)
        # set the method to "GET" from default POST because Amazon S3 only
        # serves GET requests on files. Typically POST would be used for apps
        client.calls.create(to=number, from_=TWILIO_PHONE_NUMBER,
                            url=DOMAIN+'/message', method="GET")


def post_message(code, message):
    """
    Sends a POST request to a GCP hosted page that updates what that page will return when queried for a Twilio message.
    :param code: The plain code
    :param message: The new message that Twilio should read
    :return: True if the page echos back the message indicating success, False otherwise
    """
    url = DOMAIN+"/message"
    data = {'message': message, 'code': code}
    r = requests.post(url, json=data)
    resp = r.json()['resp_message']
    return resp == message


def get_xml():
    url = DOMAIN+"/message"
    r = requests.get(url)
    print(r.content)
