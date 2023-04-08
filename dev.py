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
        self.screen_width = 800
        self.screen_height = 480
        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.info = {}
        self.frames = {}
        self.reset()

    def reset(self):
        self.info["mode"] = None
        self.info["target_temp"] = None

        if self.frames:
            for frame in self.frames:
                self.frames[frame].destroy()
        
        self.frames["initial"] = Initial(self, width = self.screen_width, height = self.screen_height)
        self.frames["mode"] = Mode(self, width = self.screen_width, height = self.screen_height)
        self.frames["adjust"] = Adjust(self, width = self.screen_width, height = self.screen_height)
        self.frames["temp"] = Temp(self, width = self.screen_width, height = self.screen_height)
        self.frames["process"] = Process(self, width = self.screen_width, height = self.screen_height)
        self.current_frame = None

        self.switch_frame("initial")

    def switch_frame(self, frame):
        if self.current_frame:
            self.current_frame.pack_forget()

        self.current_frame = self.frames[frame]
        self.current_frame.pack()

class CustomButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(borderwidth=0, highlightthickness=0)

class CustomLabel(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(font=("Helvetica", 26), background="#999999", foreground="#ffffff", padx=45, pady=20, borderwidth=0)

class Initial(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.begin_image = tk.PhotoImage(file = "resources/begin.png")
        self.begin_button = CustomButton(self, text = "Click to Begin", command = self.begin_pressed)
        # self.begin_button.pack()
        self.begin_button.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.begin_button.lift()
        self.begin_button.configure(width=100, height=50)

    def begin_pressed(self):
        self.master.switch_frame("mode")
    
class Mode(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.heat_image = tk.PhotoImage(file = "resources/heat.png")
        self.heat_button = CustomButton(self, image = self.heat_image, command = self.heat_pressed)
        self.heat_button.pack()

        self.cool_image = tk.PhotoImage(file = "resources/cool.png")
        self.cool_button = CustomButton(self, image = self.cool_image, command = self.cool_pressed)
        self.cool_button.pack()

        self.clean_image = tk.PhotoImage(file = "resources/clean.png")
        self.clean_button = CustomButton(self, image = self.clean_image, command = self.clean_pressed)
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
        self.up_image = tk.PhotoImage(file = "resources/up.png")
        self.up_image = self.up_image.subsample(10)

        self.down_image = tk.PhotoImage(file = "resources/down.png")
        self.down_image = self.down_image.subsample(10)

        self.inlet_up_button = CustomButton(self, image = self.up_image, command = self.inlet_up_pressed)
        self.inlet_up_button.pack()

        self.inlet_down_button = CustomButton(self, image = self.down_image, command = self.inlet_down_pressed)
        self.inlet_down_button.pack()

        self.outlet_up_button = CustomButton(self, image = self.up_image, command = self.outlet_up_pressed)
        self.outlet_up_button.pack()

        self.outlet_down_button = CustomButton(self, image = self.down_image, command = self.outlet_down_pressed)
        self.outlet_down_button.pack()
        
        self.next_image = tk.PhotoImage(file = "resources/next.png")
        self.next_button = CustomButton(self, image = self.next_image, command = self.next_pressed)
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
        self.up_image = tk.PhotoImage(file = "resources/up.png")
        self.up_image = self.up_image.subsample(10)

        self.down_image = tk.PhotoImage(file = "resources/down.png")
        self.down_image = self.down_image.subsample(10)

        self.temp_up_button = CustomButton(self, image = self.up_image, command = self.temp_up_pressed)
        self.temp_up_button.pack()

        self.temp_down_button = CustomButton(self, image = self.down_image, command = self.temp_down_pressed)
        self.temp_down_button.pack()
        
        self.next_image = tk.PhotoImage(file = "resources/next.png")
        self.next_button = CustomButton(self, image = self.next_image, command = self.next_pressed)
        self.next_button.pack()

    def temp_up_pressed(self):
        print("u")

    def temp_down_pressed(self):
        print("d")
    
    def next_pressed(self):
        self.master.switch_frame("process")

class Process(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.start_image = tk.PhotoImage(file = "resources/start.png")
        self.start_button = CustomButton(self, image = self.start_image, command = self.start_pressed)
        self.start_button.pack()

    def start_pressed(self):
        self.start_button.destroy()
        self.master.update()

        if self.master.info["mode"] == 2:
            self.timer_label = CustomLabel(self, text = "10 seconds remaining")
            self.timer_label.pack()
        else:
            self.current_temp_label = CustomLabel(self, text = "30 degrees celcius")
            self.current_temp_label.pack()

            self.timer_label = CustomLabel(self, text = "10 seconds elasped")
            self.timer_label.pack()

        self.master.update()

        sleep(2)
        
        self.master.reset()

app = Application()
app.mainloop()