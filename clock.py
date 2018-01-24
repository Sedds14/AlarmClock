#!/usr/bin/python

import time
import datetime
import RPi.GPIO as GPIO

from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33
from phue import Bridge
from phue import Light

def main():

  preStart()
  
  while(True):
    # Wait a quarter second (less than 1 second to prevent colon blinking getting annoying)  
    time.sleep(0.25)     
    
    if light.on clockUpdate(4) 
    # If the room light is on update time at normal 
    # brightness (normal operation)
    
    elif GPIO.input(BtnPin) is 0 clockUpdate(0) 
    # Else if the button is pressed show the 
    # time at lowest brightness setting (night operation)
    
    else clockOff() 
    # Else do not show the time. It's sleepy time.

def preStart():
  # Setup Display
  segment = SevenSegment.SevenSegment(address=0x70)
  display = HT16K33.HT16K33(address=0x70)
  # Initialize the display. Must be called once before using the display.
  segment.begin()

  # Setup GPIO Button
  BtnPin = 12 # pin12 --- button
  GPIO.setmode(GPIO.BOARD)									# Numbers GPIOs by physical location
  GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  		# Set BtnPin's mode as input 
  
  # Initialize the philips bridge
  bridge = Bridge('192.168.0.10')
  #Initialise the bedroom light
  light = Light(bridge, 'Bedroom')
	
def clockUpdate(brightness):
  # clear the buffer
  segment.clear()
  #set display brightness
  display.set_brightness(brightness)
  #Update the time
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  second = now.second
  #Set hours                                
  segment.set_digit(0, int(hour / 10))     # Tens
  segment.set_digit(1, hour % 10)          # Ones
  #Set minutes
  segment.set_digit(2, int(minute / 10))   # Tens
  segment.set_digit(3, minute % 10)        # Ones
  #Toggle colon
  segment.set_colon(second % 2)            # Toggle colon at 1Hz
  # Write the display buffer to the hardware.
  segment.write_display()	

def clockOff():
  # clear the buffer
  segment.clear()
  # The light is off so the room should be dark to achieve this effect...
  # display empty string
  segment.print_number_str("    ")
  # and set colon to off
  segment.set_colon(0)
  # Write the display buffer to the hardware.
  segment.write_display()

if__name__== "__main__:
	main()