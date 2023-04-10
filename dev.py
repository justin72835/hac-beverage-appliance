from threading import Thread, Lock
from time import sleep, perf_counter
import random
import RPi.GPIO as GPIO
import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UTME Warmer")
        # self.screen_width = self.winfo_screenwidth()
        # self.screen_height = self.winfo_screenheight()
        self.screen_width = 800
        self.screen_height = 480
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.frames = {}

        self.setup_hardware()
        self.reset()

    def setup_hardware(self):
        self.DIR_inlet = 10
        self.DIR_outlet = 16

        self.STEP_inlet = 8
        self.STEP_outlet = 18

        self.SWITCH_inlet_top = 29
        self.SWITCH_inlet_bottom = 29
        self.SWITCH_outlet_top = 29
        self.SWITCH_outlet_bottom = 29

        # communicating with stepper motors and switches
        self.ACTUATION = {
            "inlet_up" : {
                "DIR" : self.DIR_inlet,
                "STEP" : self.STEP_inlet,
                "forward" : 0,
                "reverse" : 1,
                "SWITCH" : self.SWITCH_inlet_top,
                "clicked" : False
            },
            "inlet_down" : {
                "DIR" : self.DIR_inlet,
                "STEP" : self.STEP_inlet,
                "forward" : 1,
                "reverse" : 0,
                "SWITCH" : self.SWITCH_inlet_bottom,
                "clicked" : False
            },
            "outlet_up" : {
                "DIR" : self.DIR_outlet,
                "STEP" : self.STEP_outlet,
                "forward" : 0,
                "reverse" : 1,
                "SWITCH" : self.SWITCH_outlet_top,
                "clicked" : False
            },
            "outlet_down" : {
                "DIR" : self.DIR_outlet,
                "STEP" : self.STEP_outlet,
                "forward" : 1,
                "reverse" : 0,
                "SWITCH" : self.SWITCH_outlet_bottom,
                "clicked" : False
            }
        }

        self.stepper_delay = 0.00005

        # communicating with pump motor
        self.MOTOR = 22

        # communicating with MAX6675
        self.CS = 36
        self.SCK = 40
        self.SO = 35

        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        # setting up stepper motors
        GPIO.setup(self.DIR_inlet, GPIO.OUT)
        GPIO.setup(self.DIR_outlet, GPIO.OUT)
        GPIO.setup(self.STEP_inlet, GPIO.OUT)
        GPIO.setup(self.STEP_outlet, GPIO.OUT)

        # setting up switches
        GPIO.setup(self.SWITCH_inlet_top, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.SWITCH_inlet_bottom, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.SWITCH_outlet_top, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.SWITCH_outlet_bottom, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # setting up pump motor
        GPIO.setup(self.MOTOR, GPIO.OUT)

        # setting up MAX6675
        GPIO.setup(self.CS, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(self.SCK, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.SO, GPIO.IN)

        # click checker thread
        self.click_checker_thread = Thread(target = self.click_checker, args = ())
        self.click_checker_thread.start()

        # current temperature
        self.current_temp = float('-inf')

        # update temperature thread
        self.update_temp_thread = Thread(target = self.update_temp, args = ())
        self.update_temp_thread.start()
    
    def click_checker(self):
        while True:
            # for id in self.ACTUATION:
            #     self.ACTUATION[id]["clicked"] = GPIO.input(self.ACTUATION[id]["SWITCH"])

            #     if self.ACTUATION[id]["clicked"]:
            #         self.move_tube(id)
            
            id = "inlet_up"

            self.ACTUATION[id]["clicked"] = GPIO.input(self.ACTUATION[id]["SWITCH"])

            if self.ACTUATION[id]["clicked"]:
                self.move_tube(id)


    def get_current_temp(self):
        temps = []

        for n in range(5):
            GPIO.output(self.CS, GPIO.LOW)
            sleep(0.002)
            GPIO.output(self.CS, GPIO.HIGH)
            sleep(0.22)

            GPIO.output(self.CS, GPIO.LOW)
            GPIO.output(self.SCK, GPIO.HIGH)
            sleep(0.001)
            GPIO.output(self.SCK, GPIO.LOW)

        val = 0
            
        for i in range(11, -1, -1):
            GPIO.output(self.SCK, GPIO.HIGH)
            val += (GPIO.input(self.SO) * (2 ** i))
            GPIO.output(self.SCK, GPIO.LOW)

        GPIO.output(self.SCK, GPIO.HIGH)
        error_tc = GPIO.input(self.SO)
        GPIO.output(self.SCK, GPIO.LOW)

        for i in range(2):
            GPIO.output(self.SCK, GPIO.HIGH)
            sleep(0.001)
            GPIO.output(self.SCK, GPIO.LOW)

        GPIO.output(self.CS, GPIO.HIGH)

        if error_tc != 0:
            return -self.CS

        temps.append(val * 0.23)

        return sum(temps)/len(temps)

    def update_temp(self):
        while True:
            self.current_temp = self.get_current_temp()

    def move_tube(self, id):
        GPIO.output(self.ACTUATION[id]["DIR"], self.ACTUATION[id]["forward"] if not self.ACTUATION[id]["clicked"] else self.ACTUATION[id]["reverse"])
        GPIO.output(self.ACTUATION[id]["STEP"], GPIO.HIGH)
        sleep(self.stepper_delay)
        GPIO.output(self.ACTUATION[id]["STEP"], GPIO.LOW)
        sleep(self.stepper_delay)
    
    def reverse_tube(self, id):
        self.ACTUATION[id]["clicked"] = GPIO.input(self.ACTUATION[id]["SWITCH"])

        if GPIO.input(self.ACTUATION[id]["SWITCH"]):
            self.reverse_tube(id)

        GPIO.output(self.ACTUATION[id]["DIR"], self.ACTUATION[id]["forward"])
        GPIO.output(self.ACTUATION[id]["STEP"], GPIO.HIGH)
        sleep(self.stepper_delay)
        GPIO.output(self.ACTUATION[id]["STEP"], GPIO.LOW)
        sleep(self.stepper_delay)

    def run_pump(self):
        GPIO.output(self.MOTOR, GPIO.HIGH)

    def stop_pump(self):
        GPIO.output(self.MOTOR, GPIO.LOW)

    def reset(self):
        self.mode = ""
        self.target_temp = float('-inf')

        if self.frames:
            for frame in self.frames:
                self.frames[frame].destroy()
        
        self.frames["initial"] = Initial(self)
        self.frames["mode"] = Mode(self)
        self.frames["adjust"] = Adjust(self)
        self.frames["temp"] = Temp(self)
        self.frames["process"] = Process(self)
        self.current_frame = None

        self.switch_frame("initial")

    def switch_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = self.frames[frame]
        self.current_frame.pack(fill='both', expand=True)

class CustomButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(borderwidth = 0, highlightthickness = 0, background = "#eeeeee")

class CustomLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(font = ("Calibri", 25, "bold"), borderwidth = 0, highlightthickness = 0, background = "#eeeeee")

class CustomFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background = "#eeeeee")

class Initial(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.begin_image = tk.PhotoImage(file = "resources/begin.png")
        self.begin_button = CustomButton(self, image = self.begin_image, command = self.begin_pressed)
        self.begin_button.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")

    def begin_pressed(self):
        self.master.switch_frame("mode")
    
class Mode(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.heat_image = tk.PhotoImage(file = "resources/heat.png")
        self.heat_button = CustomButton(self, image = self.heat_image, command = self.heat_pressed)
        self.heat_button.place(x = self.master.screen_width * 1 // 3, y = self.master.screen_height * 1 // 3, anchor = "center")

        self.cool_image = tk.PhotoImage(file = "resources/cool.png")
        self.cool_button = CustomButton(self, image = self.cool_image, command = self.cool_pressed)
        self.cool_button.place(x = self.master.screen_width * 2 // 3, y = self.master.screen_height * 1 // 3, anchor = "center")

        self.clean_image = tk.PhotoImage(file = "resources/clean.png")
        self.clean_button = CustomButton(self, image = self.clean_image, command = self.clean_pressed)
        self.clean_button.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 2 // 3, anchor = "center")
    
    def heat_pressed(self):
        self.master.mode = "heat"
        self.master.switch_frame("adjust")

    def cool_pressed(self):
        self.master.mode = "cool"
        self.master.switch_frame("adjust")

    def clean_pressed(self):
        self.master.mode = "clean"
        self.master.switch_frame("adjust")

class Adjust(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.is_pressed = False

        self.up_image = tk.PhotoImage(file = "resources/up.png")
        self.up_image = self.up_image

        self.down_image = tk.PhotoImage(file = "resources/down.png")
        self.down_image = self.down_image

        self.inlet_up_button = CustomButton(self, image = self.up_image)
        self.inlet_up_button.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 1 // 3, anchor = "center")
        self.inlet_up_button.bind("<ButtonPress-1>", lambda x : self.pressed("inlet_up"))
        self.inlet_up_button.bind("<ButtonRelease-1>", lambda x : self.released("inlet_up"))

        self.inlet_down_button = CustomButton(self, image = self.down_image)
        self.inlet_down_button.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 2 // 3, anchor = "center")
        self.inlet_down_button.bind("<ButtonPress-1>", lambda x : self.pressed("inlet_down"))
        self.inlet_down_button.bind("<ButtonRelease-1>", lambda x : self.released("inlet_down"))

        self.inlet_label = CustomLabel(self, text = "Right")
        self.inlet_label.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.outlet_up_button = CustomButton(self, image = self.up_image)
        self.outlet_up_button.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 1 // 3, anchor = "center")
        self.outlet_up_button.bind("<ButtonPress-1>", lambda x : self.pressed("outlet_up"))
        self.outlet_up_button.bind("<ButtonRelease-1>", lambda x : self.released("outlet_up"))

        self.outlet_down_button = CustomButton(self, image = self.down_image)
        self.outlet_down_button.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 2 // 3, anchor = "center")
        self.outlet_down_button.bind("<ButtonPress-1>", lambda x : self.pressed("outlet_down"))
        self.outlet_down_button.bind("<ButtonRelease-1>", lambda x : self.released("outlet_down"))
        
        self.outlet_label = CustomLabel(self, text = "Left")
        self.outlet_label.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.next_image = tk.PhotoImage(file = "resources/next.png")
        self.next_button = CustomButton(self, image = self.next_image, command = self.next_pressed)
        self.next_button.place(x = self.master.screen_width * 7 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")
    
    def check(self, id):
        while self.is_pressed and not self.master.ACTUATION[id]["clicked"]:
            self.master.move_tube(id)

    def pressed(self, id):
        self.is_pressed = True
        check_thread = Thread(target = self.check, args = [id])
        check_thread.start()

    def released(self, id):
        self.is_pressed = False
        
    def next_pressed(self):
        if self.master.mode == "clean":
            self.master.switch_frame("process")
        else:
            self.master.switch_frame("temp")

class Temp(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.is_pressed = False
        self.target_temp = 25

        self.up_image = tk.PhotoImage(file = "resources/up.png")
        self.up_image = self.up_image

        self.down_image = tk.PhotoImage(file = "resources/down.png")
        self.down_image = self.down_image

        self.temp_up_button = CustomButton(self, image = self.up_image)
        self.temp_up_button.place(x = self.master.screen_width * 1 // 3, y = self.master.screen_height * 1 // 3, anchor = "center")
        self.temp_up_button.bind("<ButtonPress-1>", lambda x : self.pressed(1))
        self.temp_up_button.bind("<ButtonRelease-1>", lambda x : self.released(1))

        self.temp_down_button = CustomButton(self, image = self.down_image)
        self.temp_down_button.place(x = self.master.screen_width * 1 // 3, y = self.master.screen_height * 2 // 3, anchor = "center")
        self.temp_down_button.bind("<ButtonPress-1>", lambda x : self.pressed(-1))
        self.temp_down_button.bind("<ButtonRelease-1>", lambda x : self.released(-1))

        self.temp_label = CustomLabel(self, text = f"{self.target_temp:.1f}\u00b0C")
        self.temp_label.place(x = self.master.screen_width * 1 // 3, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.next_image = tk.PhotoImage(file = "resources/next.png")
        self.next_button = CustomButton(self, image = self.next_image, command = self.next_pressed)
        self.next_button.place(x = self.master.screen_width * 2 // 3, y = self.master.screen_height * 1 // 2, anchor = "center")

    def check(self, id):
        start_time = perf_counter()
        while self.is_pressed and (self.master.current_temp < self.target_temp <= 50 and self.master.mode == "heat" or 0 <= self.target_temp < self.master.current_temp and self.master.mode == "cool"):
            self.target_temp += id
            self.temp_label.config(text = f"{self.target_temp:.1f}\u00b0C")

            if perf_counter() - start_time < 2:
                sleep(0.2)
            else:
                sleep(0.1)

    def pressed(self, id):
        self.is_pressed = True
        check_thread = Thread(target = self.check, args = [id])
        check_thread.start()

    def released(self, id):
        self.is_pressed = False

    def next_pressed(self):
        self.master.target_temp = self.target_temp
        self.master.switch_frame("process")

class Process(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.start_image = tk.PhotoImage(file = "resources/start.png")
        self.start_button = CustomButton(self, image = self.start_image, command = self.start_pressed)
        self.start_button.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")

    def start_pressed(self):
        self.start_button.destroy()
        self.master.update()
        start_time = perf_counter()

        self.master.run_pump()

        if self.master.mode == "clean":
            clean_duration = 10
        
            self.timer_label = CustomLabel(self)
            self.timer_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")

            while perf_counter() - start_time < clean_duration:
                self.timer_label.config(text = f"Time remaining: {clean_duration - int(perf_counter() - start_time)} seconds")
                self.master.update()

            self.timer_label.destroy()

        else:
            self.timer_label = CustomLabel(self)
            self.timer_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 2 // 5, anchor = "center")

            self.current_temp_label = CustomLabel(self)
            self.current_temp_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 3 // 5, anchor = "center")

            while self.master.current_temp <= self.master.target_temp and self.master.mode == "heat" or self.master.current_temp >= self.master.target_temp and self.master.mode == "cool":
                self.timer_label.config(text = f"Time elapsed: {int(perf_counter() - start_time)} seconds")
                self.current_temp_label.config(text = f"Currnet temperature: {self.master.current_temp:.1f}\u00b0C")
                self.master.update()
            
            self.timer_label.destroy()
            self.current_temp_label.destroy()

        self.master.update()
        
        while not self.master.ACTUATION["inlet_up"]["clicked"]:
            self.master.move_tube("inlet_up")

        self.master.stop_pump()

        self.end_label = CustomLabel(self, text = "Cycle Completed!")
        self.end_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")
        self.master.update()

        sleep(1)
        
        self.master.reset()

app = Application()
app.mainloop()