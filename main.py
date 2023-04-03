from threading import Thread
from time import sleep
import random
import RPi.GPIO as GPIO
import tkinter as tk

######################################
## HARDWARE ## HARDWARE ## HARDWARE ##
###################################### 

###################
###### PINS ####### 
################### 

# communicating with stepper motors
DIR_inlet = 10
DIR_outlet = 16
STEP_inlet = 8
STEP_outlet = 18

# communicating with pump motor
MOTOR = 22

# communicating with MAX6675
CS = 36
SCK = 40
SO = 35

###################
##### SETUP ####### 
###################

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)

# setting up stepper motors
GPIO.setup(DIR_inlet, GPIO.OUT)
GPIO.setup(DIR_outlet, GPIO.OUT)
GPIO.setup(STEP_inlet, GPIO.OUT)
GPIO.setup(STEP_outlet, GPIO.OUT)

# setting up pump motor
GPIO.setup(MOTOR, GPIO.OUT)
GPIO.output(MOTOR, GPIO.LOW)

# setting up MAX6675
GPIO.setup(CS, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(SCK, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(SO, GPIO.IN)

###################
#### FUNCTIONS #### 
###################

# upward
def move_up(DIR, STEP):
    GPIO.output(DIR, 0)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.0004)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.0004)

# downward
def move_down(DIR, STEP):
    GPIO.output(DIR, 1)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.0004)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.0004)

# run normal cycle
def start_cycle(desired_temperature):
    global heat_cool_global
    GPIO.output(MOTOR, GPIO.HIGH)
    current_temperature = get_current_temperature()
    while current_temperature < desired_temperature and heat_cool_global or current_temperature > desired_temperature and not heat_cool_global:
        print(current_temperature, heat_cool_global)
        pass
    GPIO.output(MOTOR, GPIO.LOW)

# run cleaning cycle
def clean_cycle(desired_temperature):
    GPIO.output(MOTOR, GPIO.HIGH)
    sleep(10)
    GPIO.output(MOTOR, GPIO.LOW)

# get current temperature over the course of a second
def get_current_temperature():
    temperatures = []

    for n in range(5):
        GPIO.output(CS, GPIO.LOW)
        sleep(0.002)
        GPIO.output(CS, GPIO.HIGH)
        sleep(0.22)

        GPIO.output(CS, GPIO.LOW)
        GPIO.output(SCK, GPIO.HIGH)
        sleep(0.001)
        GPIO.output(SCK, GPIO.LOW)

        value = 0
        
        for i in range(11, -1, -1):
            GPIO.output(SCK, GPIO.HIGH)
            value += (GPIO.input(SO) * (2 ** i))
            GPIO.output(SCK, GPIO.LOW)

        GPIO.output(SCK, GPIO.HIGH)
        error_tc = GPIO.input(SO)
        GPIO.output(SCK, GPIO.LOW)

        for i in range(2):
            GPIO.output(SCK, GPIO.HIGH)
            sleep(0.001)
            GPIO.output(SCK, GPIO.LOW)

        GPIO.output(CS, GPIO.HIGH)

        if error_tc != 0:
            return -CS

        temperatures.append(value * 0.23)

    return sum(temperatures)/len(temperatures)

######################################
## SOFTWARE ## SOFTWARE ## SOFTWARE ##
######################################

###################
### GLOBAL VARS ### 
###################  

power_global = True
heat_cool_global = True

inlet_up_global = False
inlet_down_global = False
outlet_up_global = False
outlet_down_global = False

###################
##### SETUP ####### 
###################

# create the root window
root = tk.Tk()

# root window geometry
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# threads and functions for tube actuation
def inlet_up_check():
    while inlet_up_global:
        move_up(DIR_inlet, STEP_inlet)

def inlet_down_check():
    while inlet_down_global:
        move_down(DIR_inlet, STEP_inlet)

def outlet_up_check():
    while outlet_up_global:
        move_up(DIR_outlet, STEP_outlet)

def outlet_down_check():
    while outlet_down_global:
        move_down(DIR_outlet, STEP_outlet)

###################
#### FUNCTIONS #### 
###################

# power button pressed
def power_pressed():
    global power_global
    if power_global:
        power_button.config(image=power_off_image)
        power_global = False
    else:
        power_button.config(image=power_on_image)
        power_global = True

# heat/cool button pressed
def heat_cool_pressed():
    global heat_cool_global
    if heat_cool_global:
        heat_cool_button.config(image=cool_image)
        heat_cool_global = False
    else:
        heat_cool_button.config(image=heat_image)
        heat_cool_global = True

# inlet up button pressed and released
def inlet_up_pressed(event):
    global inlet_up_global
    inlet_up_thread = Thread(target = inlet_up_check, args = ())
    inlet_up_button.config(image=inlet_up_shade_image)
    inlet_up_global = True
    inlet_up_thread.start()
def inlet_up_released(event):
    global inlet_up_global
    inlet_up_button.config(image=inlet_up_image)
    inlet_up_global = False

# inlet down button pressed and released
def inlet_down_pressed(event):
    global inlet_down_global
    inlet_down_thread = Thread(target = inlet_down_check, args = ())
    inlet_down_button.config(image=inlet_down_shade_image)
    inlet_down_global = True
    inlet_down_thread.start()
def inlet_down_released(event):
    global inlet_down_global
    inlet_down_button.config(image=inlet_down_image)
    inlet_down_global = False

# outlet up button pressed and released
def outlet_up_pressed(event):
    global outlet_up_global
    outlet_up_thread = Thread(target = outlet_up_check, args = ())
    outlet_up_button.config(image=outlet_up_shade_image)
    outlet_up_global = True
    outlet_up_thread.start()
def outlet_up_released(event):
    global outlet_up_global
    outlet_up_button.config(image=outlet_up_image)
    outlet_up_global = False

# outlet down button pressed and released
def outlet_down_pressed(event):
    global outlet_down_global
    outlet_down_thread = Thread(target = outlet_down_check, args = ())
    outlet_down_button.config(image=outlet_down_shade_image)
    outlet_down_global = True
    outlet_down_thread.start()
def outlet_down_released(event):
    global outlet_down_global
    outlet_down_button.config(image=outlet_down_image)
    outlet_down_global = False

# start button pressed
def start_pressed():
    start_button.config(image=start_shade_image)
    start_cycle(float(desired_temperature_entry.get()))
    start_button.config(image=start_image)

# clean button pressed
def clean_pressed():
    clean_button.config(image=clean_shade_image)
    clean_cycle()
    clean_button.config(image=clean_image)

# updates temperature reading every second
def update_temperature():
    while True:
        current_temperature_label.config(text = get_current_temperature())

###################
##### BUTTONS ##### 
###################  

# power button
power_on_image = tk.PhotoImage(file="assets/power_on.png")
power_off_image = tk.PhotoImage(file="assets/power_off.png")
power_button = tk.Button(root, image = power_on_image, command=power_pressed)

# heat/cool button
heat_image = tk.PhotoImage(file="assets/heat.png")
cool_image = tk.PhotoImage(file="assets/cool.png")
heat_cool_button = tk.Button(root, image = heat_image, command=heat_cool_pressed)

# up and down buttons
inlet_up_image = tk.PhotoImage(file="assets/inlet_up.png")
inlet_up_shade_image = tk.PhotoImage(file="assets/inlet_up_shade.png")
inlet_up_button = tk.Button(root, image = inlet_up_image)
inlet_up_button.bind("<ButtonPress-1>", inlet_up_pressed)
inlet_up_button.bind("<ButtonRelease-1>", inlet_up_released)

inlet_down_image = tk.PhotoImage(file="assets/inlet_down.png")
inlet_down_shade_image = tk.PhotoImage(file="assets/inlet_down_shade.png")
inlet_down_button = tk.Button(root, image = inlet_down_image)
inlet_down_button.bind("<ButtonPress-1>", inlet_down_pressed)
inlet_down_button.bind("<ButtonRelease-1>", inlet_down_released)

outlet_up_image = tk.PhotoImage(file="assets/outlet_up.png")
outlet_up_shade_image = tk.PhotoImage(file="assets/outlet_up_shade.png")
outlet_up_button = tk.Button(root, image = outlet_up_image)
outlet_up_button.bind("<ButtonPress-1>", outlet_up_pressed)
outlet_up_button.bind("<ButtonRelease-1>", outlet_up_released)

outlet_down_image = tk.PhotoImage(file="assets/outlet_down.png")
outlet_down_shade_image = tk.PhotoImage(file="assets/outlet_down_shade.png")
outlet_down_button = tk.Button(root, image = outlet_down_image)
outlet_down_button.bind("<ButtonPress-1>", outlet_down_pressed)
outlet_down_button.bind("<ButtonRelease-1>", outlet_down_released)

# start button
start_image = tk.PhotoImage(file="assets/start.png")
start_shade_image = tk.PhotoImage(file="assets/start_shade.png")
start_button = tk.Button(root, image = start_image, command=start_pressed)


# clean button
clean_image = tk.PhotoImage(file="assets/clean.png")
clean_shade_image = tk.PhotoImage(file="assets/clean_shade.png")
clean_button = tk.Button(root, image = clean_image, command=clean_pressed)

###################
##### ENTRIES ##### 
###################  

# desired temperature
desired_temperature_entry = tk.Entry(root)

###################
##### LABLES ###### 
###################

# current temperature
current_temperature_label = tk.Label(root)

###################
# FUNCTION CALLS ##
###################

# adding objects to window
current_temperature_label.pack()

desired_temperature_entry.pack()
power_button.pack()
heat_cool_button.pack()
inlet_up_button.pack()
inlet_down_button.pack()
outlet_up_button.pack()
outlet_down_button.pack()
start_button.pack()
clean_button.pack()

# update temperature thread
update_temperature_thread = Thread(target = update_temperature, args = ())
update_temperature_thread.start()

# start the tkinter event loop
root.mainloop()