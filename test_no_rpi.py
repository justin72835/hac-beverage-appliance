from threading import Thread, Lock
from time import sleep
import random
import tkinter as tk
from PIL import Image, ImageTk

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
#### FUNCTIONS #### 
###################

# upward
def move_up(DIR, STEP):
    print("up")

# downward
def move_down(DIR, STEP):
    print("down")

# run normal cycle
def start_cycle(desired_temperature):
    global heat_cool_global
    global current_temperature_global
    
    print("inside start")

    while True:
        if current_temperature_global < desired_temperature and heat_cool_global or current_temperature_global > desired_temperature and not heat_cool_global:
            print(current_temperature_global, heat_cool_global)
        else:
            break

    print("break")

# run cleaning cycle
def clean_cycle(desired_temperature):
    pass

# get current temperature over the course of a second
def get_current_temperature():
    pass

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

current_temperature_global = 0

###################
##### SETUP ####### 
###################

# create the root window
root = tk.Tk()

# root window geometry
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg='black')

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
# LOADING ASSETS ##
###################

inlet_up = Image.open('assets/New Assets/inlet_up.png')
inlet_up = inlet_up.resize((100, 80), Image.ANTIALIAS)
inlet_up = ImageTk.PhotoImage(inlet_up)

inlet_down = Image.open('assets/New Assets/inlet_down.png')
inlet_down = inlet_down.resize((100, 115), Image.ANTIALIAS)
inlet_down = ImageTk.PhotoImage(inlet_down)

inlet_up_shade = Image.open('assets/New Assets/inlet_up_shade.png')
inlet_up_shade = inlet_up_shade.resize((100, 80), Image.ANTIALIAS)
inlet_up_shade = ImageTk.PhotoImage(inlet_up_shade)

inlet_down_shade = Image.open('assets/New Assets/inlet_down_shade.png')
inlet_down_shade = inlet_down_shade.resize((100, 115), Image.ANTIALIAS)
inlet_down_shade = ImageTk.PhotoImage(inlet_down_shade)

outlet_up = Image.open('assets/New Assets/outlet_up.png')
outlet_up = outlet_up.resize((100, 80), Image.ANTIALIAS)
outlet_up = ImageTk.PhotoImage(outlet_up)

outlet_down = Image.open('assets/New Assets/outlet_down.png')
outlet_down = outlet_down.resize((100, 115), Image.ANTIALIAS)
outlet_down = ImageTk.PhotoImage(outlet_down)

outlet_up_shade = Image.open('assets/New Assets/outlet_up_shade.png')
outlet_up_shade = outlet_up_shade.resize((100, 80), Image.ANTIALIAS)
outlet_up_shade = ImageTk.PhotoImage(outlet_up_shade)

outlet_down_shade = Image.open('assets/New Assets/outlet_down_shade.png')
outlet_down_shade = outlet_down_shade.resize((100, 115), Image.ANTIALIAS)
outlet_down_shade = ImageTk.PhotoImage(outlet_down_shade)

start = Image.open('assets/New Assets/start.png')
start = start.resize((140, 75), Image.ANTIALIAS)
start = ImageTk.PhotoImage(start)

start_shade = Image.open('assets/New Assets/start_shade.png')
start_shade = start_shade.resize((140, 75), Image.ANTIALIAS)
start_shade = ImageTk.PhotoImage(start_shade)

clean = Image.open('assets/New Assets/clean.png')
clean = clean.resize((140, 80), Image.ANTIALIAS)
clean = ImageTk.PhotoImage(clean)

clean_shade = Image.open('assets/New Assets/clean_shade.png')
clean_shade = clean_shade.resize((140, 80), Image.ANTIALIAS)
clean_shade = ImageTk.PhotoImage(clean_shade)

power_on = Image.open('assets/power_on.png')
power_on = power_on.resize((100, 80), Image.ANTIALIAS)
power_on = ImageTk.PhotoImage(power_on)

power_off = Image.open('assets/power_off.png')
power_off = power_off.resize((100, 80), Image.ANTIALIAS)
power_off = ImageTk.PhotoImage(power_off)

cool = Image.open('assets/cool.png')
cool = cool.resize((100, 80), Image.ANTIALIAS)
cool = ImageTk.PhotoImage(cool)

heat = Image.open('assets/heat.png')
heat = heat.resize((100, 80), Image.ANTIALIAS)
heat = ImageTk.PhotoImage(heat)

###################
#### FUNCTIONS #### 
###################

# power button pressed
def power_pressed():
    global power_global
    if power_global:
        power_button.config(image=power_off, borderwidth=0, highlightthickness=0)
        power_global = False
    else:
        power_button.config(image=power_on, borderwidth=0, highlightthickness=0)
        power_global = True

# heat/cool button pressed
def heat_cool_pressed():
    global heat_cool_global
    if heat_cool_global:
        heat_cool_button.config(image=cool, borderwidth=0, highlightthickness=0)
        heat_cool_global = False
    else:
        heat_cool_button.config(image=heat, borderwidth=0, highlightthickness=0)
        heat_cool_global = True

# inlet up button pressed and released
def inlet_up_pressed(event):
    global inlet_up_global
    inlet_up_thread = Thread(target = inlet_up_check, args = ())
    inlet_up_button.config(image=inlet_up_shade, borderwidth=0, highlightthickness=0)
    inlet_up_global = True
    inlet_up_thread.start()
def inlet_up_released(event):
    global inlet_up_global
    inlet_up_button.config(image=inlet_up, borderwidth=0, highlightthickness=0)
    inlet_up_global = False

# inlet down button pressed and released
def inlet_down_pressed(event):
    global inlet_down_global
    inlet_down_thread = Thread(target = inlet_down_check, args = ())
    inlet_down_button.config(image=inlet_down_shade, borderwidth=0, highlightthickness=0)
    inlet_down_global = True
    inlet_down_thread.start()
def inlet_down_released(event):
    global inlet_down_global
    inlet_down_button.config(image=inlet_down, borderwidth=0, highlightthickness=0)
    inlet_down_global = False

# outlet up button pressed and released
def outlet_up_pressed(event):
    global outlet_up_global
    outlet_up_thread = Thread(target = outlet_up_check, args = ())
    outlet_up_button.config(image=outlet_up_shade, borderwidth=0, highlightthickness=0)
    outlet_up_global = True
    outlet_up_thread.start()
def outlet_up_released(event):
    global outlet_up_global
    outlet_up_button.config(image=outlet_up, borderwidth=0, highlightthickness=0)
    outlet_up_global = False

# outlet down button pressed and released
def outlet_down_pressed(event):
    global outlet_down_global
    outlet_down_thread = Thread(target = outlet_down_check, args = ())
    outlet_down_button.config(image=outlet_down_shade, borderwidth=0, highlightthickness=0)
    outlet_down_global = True
    outlet_down_thread.start()
def outlet_down_released(event):
    global outlet_down_global
    outlet_down_button.config(image=outlet_down, borderwidth=0, highlightthickness=0)
    outlet_down_global = False

# start button pressed
def start_pressed():
    print('start')
    start_button.config(image=start_shade, borderwidth=0, highlightthickness=0)
    start_cycle_thread = Thread(target = start_cycle, args = [float(desired_temperature_entry.get())])
    start_cycle_thread.start()
    start_button.config(image=start, borderwidth=0, highlightthickness=0)

# clean button pressed
def clean_pressed():
    clean_button.config(image=clean_shade,borderwidth=0, highlightthickness=0)
    clean_cycle()
    clean_button.config(image=clean, borderwidth=0, highlightthickness=0)

# updates temperature reading every second
def update_temperature():
    while True:
        global current_temperature_global
        sleep(1)
        current_temperature_global += 1
        current_temperature_label.config(text = current_temperature_global)


###################
##### BUTTONS ##### 
###################  

# power button
power_button = tk.Button(root, image = power_on, borderwidth=0, highlightthickness=0, command=power_pressed)

# heat/cool button
heat_cool_button = tk.Button(root, image = heat, borderwidth=0, highlightthickness=0, command=heat_cool_pressed)

# up and down buttons
inlet_up_button = tk.Button(root, image = inlet_up, borderwidth=0, highlightthickness=0)
inlet_up_button.bind("<ButtonPress-1>", inlet_up_pressed)
inlet_up_button.bind("<ButtonRelease-1>", inlet_up_released)

inlet_down_button = tk.Button(root, image = inlet_down, borderwidth=0, highlightthickness=0)
inlet_down_button.bind("<ButtonPress-1>", inlet_down_pressed)
inlet_down_button.bind("<ButtonRelease-1>", inlet_down_released)

outlet_up_button = tk.Button(root, image = outlet_up, borderwidth=0, highlightthickness=0)
outlet_up_button.bind("<ButtonPress-1>", outlet_up_pressed)
outlet_up_button.bind("<ButtonRelease-1>", outlet_up_released)

outlet_down_button = tk.Button(root, image = outlet_down, borderwidth=0, highlightthickness=0)
outlet_down_button.bind("<ButtonPress-1>", outlet_down_pressed)
outlet_down_button.bind("<ButtonRelease-1>", outlet_down_released)

# start button
start_button = tk.Button(root, image = start, borderwidth=0, highlightthickness=0, command=start_pressed)

# clean button
clean_button = tk.Button(root, image = clean, borderwidth=0, highlightthickness=0, command=clean_pressed)

###################
##### ENTRIES ##### 
###################  

# desired temperature
desired_temparature_text = tk.Label(root, text="Enter Desired Temperature:")
desired_temperature_entry = tk.Entry(root)

###################
##### LABLES ###### 
###################

# current temperature
current_temperature_text = tk.Label(root, text="Current Temperature!")
current_temperature_label = tk.Label(root)

###################
# FUNCTION CALLS ##
###################

x = screen_width * 0.2
y = screen_height * 0.2

# adding objects to window
power_button.place(x=x, y=y)
heat_cool_button.place(x=x, y=y+100)

inlet_up_button.place(x=x+190, y=y)
inlet_down_button.place(x=x+190, y=y+80)
outlet_up_button.place(x=x+280, y=y)
outlet_down_button.place(x=x+280, y=y+80)

current_temperature_text.place(x=x+470, y=y+20)
current_temperature_label.place(x=x+470, y=y+50)
desired_temparature_text.place(x=x+470, y=y+120)
desired_temperature_entry.place(x=x+470, y=y+150)

start_button.place(x=x+690, y=y)
clean_button.place(x=x+690, y=y+100)

# update temperature thread
current_temperature_lock = Lock()
update_temperature_thread = Thread(target = update_temperature, args = ())
update_temperature_thread.start()

# start the tkinter event loop
root.mainloop()