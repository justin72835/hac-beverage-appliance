from threading import Thread, Lock
from time import sleep, perf_counter
import random
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
        # communicating with stepper motors
        self.DIR_inlet = 10
        self.DIR_outlet = 16
        self.STEP_inlet = 8
        self.STEP_outlet = 18

        # communicating with switches
        self.SWITCH_inlet_top = 0
        self.SWITCH_inlet_bottom = 0
        self.SWITCH_outlet_top = 0
        self.SWITCH_outlet_bottom = 0

        # communicating with pump motor
        self.MOTOR = 22

        # communicating with MAX6675
        self.CS = 36
        self.SCK = 40
        self.SO = 35

        # checks for switch contact
        self.inlet_top_clicked = False
        self.inlet_bottom_clicked = False
        self.outlet_top_clicked = False
        self.outlet_bottom_clicked = False

        # current temperature
        self.current_temp = float('-inf')

        # update temperature thread
        self.update_temp_thread = Thread(target = self.update_temp, args = ())
        self.update_temp_thread.start()
    
    def get_current_temp(self):
        return random.randint(0, 50)

    def update_temp(self):
        i = 0
        while True:
            self.current_temp = i
            i += 1
            sleep(1)

    def reset(self):
        self.mode = float('-inf')
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

    def move_tube(self, DIR, STEP, direction):
        if direction:
            print("down")
        else:
            print("up")

    def run_pump(self):
        print("motor pulse")

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
        self.master.mode = 0
        self.master.switch_frame("adjust")

    def cool_pressed(self):
        self.master.mode = 1
        self.master.switch_frame("adjust")

    def clean_pressed(self):
        self.master.mode = 2
        self.master.switch_frame("adjust")

class Adjust(CustomFrame):
    def __init__(self, master):
        super().__init__(master)
        self.is_pressed = False

        self.button_map = {
            0 : [self.master.DIR_inlet, self.master.STEP_inlet, 0, self.master.SWITCH_inlet_top],
            1 : [self.master.DIR_inlet, self.master.STEP_inlet, 1, self.master.SWITCH_inlet_bottom],
            2 : [self.master.DIR_outlet, self.master.STEP_outlet, 0, self.master.SWITCH_outlet_top],
            3 : [self.master.DIR_outlet, self.master.STEP_outlet, 1, self.master.SWITCH_outlet_bottom],
        }

        self.up_image = tk.PhotoImage(file = "resources/up.png")
        self.up_image = self.up_image

        self.down_image = tk.PhotoImage(file = "resources/down.png")
        self.down_image = self.down_image

        self.inlet_up_button = CustomButton(self, image = self.up_image)
        self.inlet_up_button.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 1 // 3, anchor = "center")
        self.inlet_up_button.bind("<ButtonPress-1>", lambda x : self.pressed(0))
        self.inlet_up_button.bind("<ButtonRelease-1>", lambda x : self.released(0))

        self.inlet_down_button = CustomButton(self, image = self.down_image)
        self.inlet_down_button.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 2 // 3, anchor = "center")
        self.inlet_down_button.bind("<ButtonPress-1>", lambda x : self.pressed(1))
        self.inlet_down_button.bind("<ButtonRelease-1>", lambda x : self.released(1))

        self.inlet_label = CustomLabel(self, text = "Right")
        self.inlet_label.place(x = self.master.screen_width * 4 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.outlet_up_button = CustomButton(self, image = self.up_image)
        self.outlet_up_button.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 1 // 3, anchor = "center")
        self.outlet_up_button.bind("<ButtonPress-1>", lambda x : self.pressed(2))
        self.outlet_up_button.bind("<ButtonRelease-1>", lambda x : self.released(2))

        self.outlet_down_button = CustomButton(self, image = self.down_image)
        self.outlet_down_button.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 2 // 3, anchor = "center")
        self.outlet_down_button.bind("<ButtonPress-1>", lambda x : self.pressed(3))
        self.outlet_down_button.bind("<ButtonRelease-1>", lambda x : self.released(3))
        
        self.outlet_label = CustomLabel(self, text = "Left")
        self.outlet_label.place(x = self.master.screen_width * 2 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.next_image = tk.PhotoImage(file = "resources/next.png")
        self.next_button = CustomButton(self, image = self.next_image, command = self.next_pressed)
        self.next_button.place(x = self.master.screen_width * 7 // 9, y = self.master.screen_height * 1 // 2, anchor = "center")
    
    def check(self, id):
        while self.is_pressed:
            self.master.move_tube(self.button_map[id][0], self.button_map[id][1], self.button_map[id][2])
            sleep(0.2)

    def pressed(self, id):
        self.is_pressed = True
        check_thread = Thread(target = self.check, args = [id])
        check_thread.start()

    def released(self, id):
        self.is_pressed = False
        print("released")
        
    def next_pressed(self):
        if self.master.mode == 2:
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
        while self.is_pressed and 0 <= self.target_temp + id <= 50:
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
        print("released")

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

        if self.master.mode == 2:
            clean_duration = 10
        
            self.timer_label = CustomLabel(self)
            self.timer_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")

            while perf_counter() - start_time < clean_duration:
                self.timer_label.config(text = f"Time remaining: {clean_duration - int(perf_counter() - start_time)} seconds")
                self.master.update()
                self.master.run_pump()

            self.timer_label.destroy()

        else:
            self.timer_label = CustomLabel(self)
            self.timer_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 2 // 5, anchor = "center")

            self.current_temp_label = CustomLabel(self)
            self.current_temp_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 3 // 5, anchor = "center")

            while self.master.current_temp <= self.master.target_temp and self.master.mode == 0 or self.master.current_temp <= self.master.target_temp and self.master.mode == 1:
                self.timer_label.config(text = f"Time elapsed: {int(perf_counter() - start_time)} seconds")
                self.current_temp_label.config(text = f"Currnet temperature: {self.master.current_temp:.1f}\u00b0C")
                self.master.update()
                self.master.run_pump()
            
            self.timer_label.destroy()
            self.current_temp_label.destroy()

        self.master.update()

        self.end_label = CustomLabel(self, text = "Cycle Completed!")
        self.end_label.place(x = self.master.screen_width * 1 // 2, y = self.master.screen_height * 1 // 2, anchor = "center")

        self.master.update()

        sleep(1)
        
        self.master.reset()

app = Application()
app.mainloop()