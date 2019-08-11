import requests


def create_raw_message(code):
    if code is None:
        return "There was an internal error. No message could be generated."

    number_map = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
                  '8': 'eight', '9': 'nine', '0': 'zero'}
    code_str = ''
    for digit in str(code):
        code_str = code_str + ' ' + number_map[digit]
    return "Good morning! To turn off the alarm, enter code" + code_str + ". Again, that's code" + code_str + \
           ". One more time, code" + code_str + ". Have a great day!"


def get_twilio_message(code):
    message = create_raw_message(code)

    url = 'https://phone-call-alarm.appspot.com/message'
    data = {'message': message, 'code': code}
    requests.post(url, json=data)
    return requests.get(url).content
