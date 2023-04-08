from threading import Thread, Lock
from time import sleep
import random
import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UTME Warmer")
        # self.screen_width = self.winfo_screenwidth()
        # self.screen_height = self.winfo_screenheight()
        # self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.geometry("800x480")

        self.info = {}
        self.info["mode"] = None
        self.info["target_temp"] = None

        self.frames = {}
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
        self.current_frame.pack()
    
class Initial(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.begin_button = tk.Button(self, text = "Click to get started!", command = lambda: master.switch_frame("mode"))
        self.begin_button.pack()
    
class Mode(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.heat_button = tk.Button(self, text = "Heat", command = self.heat_pressed)
        self.heat_button.pack()

        self.cool_button = tk.Button(self, text = "Cool", command = self.cool_pressed)
        self.cool_button.pack()

        self.clean_button = tk.Button(self, text = "Clean", command = self.clean_pressed)
        self.clean_button.pack()
    
    def heat_pressed(self):
        self.master.info["mode"] = 0
        self.master.switch_frame("adjust")

    def cool_pressed(self):
        self.master.info["mode"] = 1
        self.master.switch_frame("adjust")

    def clean_pressed(self):
        self.master.info["mode"] = 2
        self.master.switch_frame("adjust")

class Adjust(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.inlet_up_button = tk.Button(self, text = "Inlet Up", command = self.inlet_up_pressed)
        self.inlet_up_button.pack()

        self.inlet_down_button = tk.Button(self, text = "Inlet Down", command = self.inlet_down_pressed)
        self.inlet_down_button.pack()

        self.outlet_up_button = tk.Button(self, text = "Outlet Up", command = self.outlet_up_pressed)
        self.outlet_up_button.pack()

        self.outlet_down_button = tk.Button(self, text = "Outlet Down", command = self.outlet_down_pressed)
        self.outlet_down_button.pack()
        
        self.next_button = tk.Button(self, text = "Next", command = self.next_pressed)
        self.next_button.pack()
    
    def inlet_up_pressed(self):
        print("u")

    def inlet_down_pressed(self):
        print("d")

    def outlet_up_pressed(self):
        print("u")

    def outlet_down_pressed(self):
        print("d")

    def next_pressed(self):
        if self.master.info["mode"] == 2:
            self.master.switch_frame("process")
        else:
            self.master.switch_frame("temp")

class Temp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.target_temp_entry = tk.Entry(self)
        self.target_temp_entry.pack()
        
        self.next_button = tk.Button(self, text = "Next", command = self.next_pressed)
        self.next_button.pack()
    
    def next_pressed(self):
        self.master.switch_frame("process")

class Process(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.start_button = tk.Button(self, text = "Start Process", command = self.start_pressed)
        self.start_button.pack()

    def start_pressed(self):
        # self.start_button.destroy()
        # print("should be forgotten")

        if self.master.info["mode"] == 2:
            self.timer_label = tk.Label(self, text = "10 seconds remaining")
            self.timer_label.pack()
        else:
            self.current_temp_label = tk.Label(self, text = "30 degrees celcius")
            self.current_temp_label.pack()

            self.timer_label = tk.Label(self, text = "10 seconds elasped")
            self.timer_label.pack()

        self.master.update()

        sleep(2)
        
        self.master.info["mode"] = None
        self.master.info["target_temp"] = None
        self.master.switch_frame("initial")

app = Application()
app.mainloop()