import argparse
import requests
from secrets import *
from twilio.rest import Client
from sys import exit

ALL_ARGS = None


def compile_joke():
    # get joke from api
    data = requests.get(
        url='https://official-joke-api.appspot.com/jokes/general/random'
    ).json()

    print('Daily Reminder!\n{}...\n{}\n'.format(data[0]['setup'], data[0]['punchline']))


def send_text(text):
    text = compile_joke() + text    # prepend joke to message
    client = Client(account_sid_secret, auth_token_secret)
    message = client.messages \
                .create(
                     body=text,
                     from_=twilio_phone,
                     to=phone_number
                 )
    print(message.sid)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shoots text with joke")
    parser.add_argument('--msg', type=str, help='Message to text', default='None Provided')
    ALL_ARGS = parser.parse_args()
    # sanitize
    if ALL_ARGS.msg == 'None Provided':
        print('No message provided...\nExiting...')
        exit(0)
    else:
        send_text(ALL_ARGS.msg)
