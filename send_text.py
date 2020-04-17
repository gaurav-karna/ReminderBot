import argparse
import requests
from datetime import timedelta, datetime as dt
from secrets import *
from twilio.rest import Client
from sys import exit
from time import sleep
from pytz import timezone

ALL_ARGS = None
TODAY_SENT = False


def compile_joke():
    # get joke from api
    data = requests.get(
        url='https://official-joke-api.appspot.com/jokes/general/random'
    ).json()
    return 'Daily Reminder!\n{}...\n{}\n'.format(data[0]['setup'], data[0]['punchline'])


def send_text(text):
    text = compile_joke() + text + '\n\nMade with love, at https://github.com/gaurav-karna/ReminderBot <3'  # prepend joke to message
    client = Client(account_sid_secret, auth_token_secret)
    message = client.messages \
                .create(
                     body=text,
                     from_=twilio_phone,
                     to=phone_number
                 )
    print(message.sid)


def sanity():
    if ALL_ARGS.hour > 23 or ALL_ARGS.hour < 0:
        print('Error in hour provided, must be >= 0 and <= 23')
        exit(0)
    if ALL_ARGS.min > 59 or ALL_ARGS.min < 0:
        print('Error in minute provided, must be >= 0 and <= 59')
        exit(0)
    if ALL_ARGS.msg == 'None Provided':
        print('No message provided...\nExiting...')
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shoots text with joke, daily in EST")
    parser.add_argument('--hour', help='hour in EST', type=int, required=True)
    parser.add_argument('--min', help='min of hour, default = 0', type=int, default=0)
    parser.add_argument('--msg', type=str, help='Message to text', default='None Provided')
    ALL_ARGS = parser.parse_args()

    # sanitize
    sanity()

    # execute until stopped
    while True:
        print('Checking time...', end='\r')
        # have datetime functionality
        current = dt.now(timezone('America/Montreal')).time()
        if (current.hour == ALL_ARGS.hour
                and (
                    # +/- 1 minute margin
                    abs(current.minute - ALL_ARGS.min) < 2
                )
        ):
            print('\nValid Time...')
            # valid time to send, not sent yet
            if not TODAY_SENT:
                print('Sending Text...')
                TODAY_SENT = True
                send_text(ALL_ARGS.msg)
            else:
                # valid time to send, sent already, sleep for 3 minutes to escape margin
                TODAY_SENT = False      # ready to send the next day
                continue_timer = 180
                while continue_timer > 0:
                    print('Text already sent at {}, continuing in {}...'.format(current, continue_timer), end='\r')
                    sleep(1)
                    continue_timer -= 1
                print()  # Refresh caret return
        # Not valid time, wait a minute
        continue_timer = 60
        while continue_timer > 0:
            print('Not time yet - {}, continuing in {}...'.format(current, continue_timer), end='\r')
            sleep(1)
            continue_timer -= 1
