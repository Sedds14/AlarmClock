#!/usr/bin/python

import time
import datetime
import RPi.GPIO as GPIO

from Adafruit_LED_Backpack import SevenSegment
from Adafruit_LED_Backpack import HT16K33
from phue import Bridge
from phue import Light

# Setup Display
segment = SevenSegment.SevenSegment(address=0x70)
display = HT16K33.HT16K33(address=0x70)

# Setup GPIO Button
BtnPin = 12 # pin12 --- button
GPIO.setmode(GPIO.BOARD)									# Numbers GPIOs by physical location
GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  		# Set BtnPin's mode as input 

# Initialize the display. Must be called once before using the display.
segment.begin()

# Initialize the philips bridge
bridge = Bridge('192.168.0.10')
#Initialise the bedroom light
light = Light(bridge, 'Bedroom')

#print "Press CTRL+Z to exit"
# Continually update the time on a 4 char, 7-segment display

while(True):
	# Wait a quarter second (less than 1 second to prevent colon blinking getting annoying)  
	time.sleep(0.25)

	# clear the buffer
	segment.clear()

	#Update the time
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	second = now.second
	switch_on = GPIO.input(BtnPin)
	print switch_on

	if light.on:
		print light.on
		#set display brightness
		display.set_brightness(4)
		#Set hours                                
		segment.set_digit(0, int(hour / 10))     # Tens
		segment.set_digit(1, hour % 10)          # Ones
		#Set minutes
		segment.set_digit(2, int(minute / 10))   # Tens
		segment.set_digit(3, minute % 10)        # Ones
		#Toggle colon
		segment.set_colon(second % 2)              # Toggle colon at 1Hz
	
	elif switch_on is 0:
	
		print "The button is pressed"
		#set display brightness
		display.set_brightness(0)
		#Set hours                                
		segment.set_digit(0, int(hour / 10))     # Tens
		segment.set_digit(1, hour % 10)          # Ones
		#Set minutes
		segment.set_digit(2, int(minute / 10))   # Tens
		segment.set_digit(3, minute % 10)        # Ones
		#Toggle colon
		segment.set_colon(second % 2)              # Toggle colon at 1Hz
	
	else:
		print light.on
		# The light is off so the room should be dark
		# display empty string
		segment.print_number_str("    ")
		#set colon to off
		segment.set_colon(0)
	
	# Write the display buffer to the hardware.  This must be called to
	# update the actual display LEDs.
	segment.write_display()	
 
def clockUpdate(brightness):
	
