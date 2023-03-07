import RPi.GPIO as GPIO
from time import sleep
import keyboard as kb

# Direction pin from controller
DIR = 10

# Step pin from controller
STEP = 8

# 0/1 used to signify clockwise or counterclockwise.
CW = 1
CCW = 0

# Setup pin layout on PI
GPIO.setmode(GPIO.BOARD)

# Establish Pins in software
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

try:
	# Run forever.
	while True:
		while kb.is_pressed('u'):
			GPIO.output(DIR,CW)
			GPIO.output(STEP, GPIO.HIGH)
			sleep(.005)
			GPIO.output(STEP,GPIO.LOW)
			sleep(.005)
		while kb.is_pressed('d'):
			GPIO.output(DIR,CCW)
			GPIO.output(STEP, GPIO.HIGH)
			sleep(.005)
			GPIO.output(STEP,GPIO.LOW)
			sleep(.005)

# Once finished clean everything up

except KeyboardInterrupt:
	print("cleanup")
	GPIO.cleanup()
