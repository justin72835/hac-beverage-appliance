# global vars
clicked = False

DIR_inlet = 0
STEP_inlet = 0

SWITCH = 22
GPIO.setup(SWITCH, GPIO.IN)

# run normal cycle
def start_cycle(desired_temperature):
    global heat_cool_global
    global current_temperature_global
    print("<start_cycle function> Cycle has been started.")

    GPIO.output(MOTOR, GPIO.HIGH)
    while current_temperature_global < desired_temperature and heat_cool_global or current_temperature_global > desired_temperature and not heat_cool_global:
        print("<start_cycle function> Inside while loop. Temperature at", current_temperature_global, "C")
        sleep(1)

    print("<start_cycle function> Cycle has ended. Desired temperature has been reached.")

    # input tube goes up until switch is True
    while not clicked:
        move_up(DIR_inlet, STEP_inlet)

    sleep(5)

    GPIO.output(MOTOR, GPIO.LOW)


def move_down(DIR, STEP):
    pass

def move_up(DIR, STEP):
    pass

# thread that receives signal from switch and updates global var
def switch_checker():
    while True:
        clicked = GPIO.input(SWITCH)

        if clicked:
            move_down(DIR_inlet, STEP_inlet)




#     while True:
#         while switch_pressed():
#             move_down(DIR_inlet, STEP_inlet)
    
# def switch_pressed():
#     # random rpi code
#     pass

        
