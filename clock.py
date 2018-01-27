"""""
clock.py

To be deployed on a WiFi enabled RPi as a digital alarm clock.
Peripherals
    - Adafruit 7 Segment Display with backpack
    - Button - on pin 12
    - Connection to Philips Hue Bridge through WiFi network

Current functionality
    - Tells the time!
    - Dark when hue light in my room is off
    - Low light setting shows time on button press

To Do:
    - Alarm: Needs a speaker hacking onto it and a connection to google
      calender
    - Battery backup?
    - Mic, privacy switch and button for alexa?
    - A case!
    - Wake up alarm that turns up the lights gradually before waking

"""""

import time
import datetime
import RPi.GPIO as GPIO
import httplib2
import os

from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33
from phue import Bridge
from phue import Light


def main():
    """
    Sets up periferals and then begins loop
    """

    # Setup Display
    segment = SevenSegment.SevenSegment(address=0x70)
    display = HT16K33.HT16K33(address=0x70)
    # Initialize the display. Must be called once before using the display.
    segment.begin()

    # Setup GPIO Button
    # pin12 --- button
    button_pin = 12
    # Numbers GPIOs by physical location
    GPIO.setmode(GPIO.BOARD)
    # Set button_pin's mode as input
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

    # Initialize the philips bridge
    bridge = Bridge('192.168.0.10')
    # Initialise the bedroom light
    light = Light(bridge, 'Bedroom')

    loop()


def loop():
    """
    This is the main loop, it loops every 0.25 secs
    and calls other functions to update the display
    according to the user inputs
    """

    while(True):
        # Wait a quarter second (less than 1 second to prevent colon
        # blinking getting annoying)  
        time.sleep(0.25)          
        if light.on:
            clockUpdate(4)
        # If the room light is on update time at normal
        # brightness (normal operation)
        elif GPIO.input(BtnPin) is 0:
            clockUpdate(0)
        # Else if the button is pressed show the
        # time at lowest brightness setting (night operation)
        else:
            clockOff()
        # Else do not show the time. It's sleepy time.


def clock_update(brightness):
    """
    Updates the clock with the current time.
    Arguments:
        brightness - INT from 0-14 setting LED bridgtness
    Returns:
        NULL
    """

    # clear the buffer
    segment.clear()
    # set display brightness
    display.set_brightness(brightness)
    # Update the time
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    # Set hours
    segment.set_digit(0, int(hour / 10))     # Tens
    segment.set_digit(1, hour % 10)          # Ones
    # Set minutes
    segment.set_digit(2, int(minute / 10))   # Tens
    segment.set_digit(3, minute % 10)        # Ones
    # Toggle colon
    segment.set_colon(second % 2)            # Toggle colon at 1Hz
    # Write the display buffer to the hardware.
    segment.write_display()	


def clock_off():
    """
    This function turns off the display by printing an empty string and turning
    off the colon.
    """
    # clear the buffer
    segment.clear()
    # The light is off so the room should be dark to achieve this effect...
    # display empty string
    segment.print_number_str("    ")
    # and set colon to off
    segment.set_colon(0)
    # Write the display buffer to the hardware.
    segment.write_display()


def get_credentials():
    """
    This has been lifted from the google example
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json',
                                              'https://www.googleapis.com/auth/calendar.readonly')
        flow.user_agent = 'clock.py'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def is_next_event(calendar_name, event_name, target_time):
    """Is it time for this type of alarm?

    Creates a Google Calendar API service object and gets the next event on a
    certain calendar, with a partiular event name, following a particular time.
    """
    # Get credentials and authorise
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print('Getting the upcoming 10 events')
    events_result = service.events().list(
        calendarId=calendar_name, timeMin=target_time, maxResults=1, 
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == "__main__":
    main()
