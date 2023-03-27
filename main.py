import tkinter as tk
import RPi.GPIO as GPIO
from time import sleep
import random

######################################
## HARDWARE ## HARDWARE ## HARDWARE ##
###################################### 

###################
###### PINS ####### 
################### 

DIR_inlet = 10
DIR_outlet = 10

STEP_inlet = 8
STEP_outlet = 8

###################
##### SETUP ####### 
###################

GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(DIR_inlet, GPIO.OUT)
GPIO.setup(DIR_outlet, GPIO.OUT)

GPIO.setup(STEP_inlet, GPIO.OUT)
GPIO.setup(STEP_outlet, GPIO.OUT)

###################
#### FUNCTIONS #### 
###################

def move_cw(DIR, STEP):
    GPIO.output(DIR, 1)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.005)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.005)

def move_ccw(DIR, STEP):
    GPIO.output(DIR, 0)
    GPIO.output(STEP, GPIO.HIGH)
    sleep(.005)
    GPIO.output(STEP, GPIO.LOW)
    sleep(.005)

######################################
## SOFTWARE ## SOFTWARE ## SOFTWARE ##
######################################

###################
### GLOBAL VARS ### 
###################  

power_global = True
heat_cool_global = True
start_global = True
clean_global = True

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
    inlet_up_button.config(image=inlet_up_shade_image)
    move_ccw(DIR_inlet, STEP_inlet)
def inlet_up_released(event):
    inlet_up_button.config(image=inlet_up_image)

# inlet down button pressed and released
def inlet_down_pressed(event):
    inlet_down_button.config(image=inlet_down_shade_image)
    move_cw(DIR_inlet, STEP_inlet)
def inlet_down_released(event):
    inlet_down_button.config(image=inlet_down_image)

# outlet up button pressed and released
def outlet_up_pressed(event):
    outlet_up_button.config(image=outlet_up_shade_image)
    move_ccw(DIR_outlet, STEP_outlet)
def outlet_up_released(event):
    outlet_up_button.config(image=outlet_up_image)

# outlet down button pressed and released
def outlet_down_pressed(event):
    outlet_down_button.config(image=outlet_down_shade_image)
    move_cw(DIR_outlet, STEP_outlet)
def outlet_down_released(event):
    outlet_down_button.config(image=outlet_down_image)

# start button pressed
def start_pressed():
    global start_global
    if start_global:
        start_button.config(image=start_shade_image)
        start_global = False
    else:
        start_button.config(image=start_image)
        start_global = True

# clean button pressed
def clean_pressed():
    global clean_global
    if clean_global:
        clean_button.config(image=clean_shade_image)
        clean_global = False
    else:
        clean_button.config(image=clean_image)
        clean_global = True

# displays current temperature reading
def update_temperature():
    # Update the timer label
    current_temperature.config(text = random.randint(50, 100))

    # Call this function again after 1000 milliseconds (1 second)
    root.after(1000, update_temperature)

###################
##### WINDOW ###### 
###################

# create the root window
root = tk.Tk()

# root window geometry
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

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
desired_temp_entry = tk.Entry(root)

###################
##### LABLES ###### 
###################

# current temperature
current_temperature = tk.Label(root)

###################
# FUNCTION CALLS ##
###################

# displays current temperature reading
update_temperature()

# adding objects to window
power_button.pack()
heat_cool_button.pack()
inlet_up_button.pack()
inlet_down_button.pack()
outlet_up_button.pack()
outlet_down_button.pack()
start_button.pack()
clean_button.pack()
desired_temp_entry.pack()
current_temperature.pack()

# start the tkinter event loop
root.mainloop()