import tkinter as tk
import time
import random

def button_clicked():
    print(button_on_off.cget('image'))
    if button_on_off.cget('image') is button_on_image:
        button_on_off.config(image=button_off_image)
        print("chNGE")
    else:
        button_on_off.config(image=button_off_image)
        print("ELSE")



def start():
    print(entry_desired_temp.get())

# Create the root window
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

button_on_image = tk.PhotoImage(file="assets/on_button.png")
button_off_image = tk.PhotoImage(file="assets/off_button.png")

# Create buttons
button_on_off = tk.Button(root, image = button_on_image, command=button_clicked)
button_heating_cooling = tk.Button(root, text="Heating/Cooling", command=button_clicked)
# button_inlet_up = tk.Button(root, text="Inlet Up", command=button_clicked)
# button_inlet_down = tk.Button(root, text="Inlet Down", command=button_clicked)
# button_outlet_up = tk.Button(root, text="Outlet Up", command=button_clicked)
# button_outlet_down = tk.Button(root, text="Outlet Down", command=button_clicked)
button_start = tk.Button(root, text="Start", command=start)
# button_clean = tk.Button(root, text="Clean", command=button_clicked)

# Create entry
entry_desired_temp = tk.Entry(root)



# Create a live label with the current temperature
current_temperature = tk.Label(root, text="Hello, World!")

# Define a function to update the timer
def update_temperature():
    # Update the timer label
    current_temperature.config(text = random.randint(50, 100))

    # Call this function again after 1000 milliseconds (1 second)
    root.after(1000, update_temperature)

# Call the update_timer() function to start the timer
update_temperature()



# Pack the label and button widgets into the window
current_temperature.pack()

button_on_off.pack()
button_heating_cooling.pack()

button_start.pack()

entry_desired_temp.pack()








# Start the tkinter event loop
root.mainloop()