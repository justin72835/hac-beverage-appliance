import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep

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

def move_cw():
    GPIO.output(DIR, CW)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.005)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.005)

def move_ccw():
    GPIO.output(DIR, CCW)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.005)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.005)

root = tk.Tk()
root.title("Stepper Motor Control")

button_cw = tk.Button(root, text="Clockwise", command=move_cw)
button_cw.pack()

button_ccw = tk.Button(root, text="Counter-Clockwise", command=move_ccw)
button_ccw.pack()

root.mainloop()

# Once finished clean everything up
GPIO.cleanup()