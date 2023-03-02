import tkinter as tk

def button_clicked():
    label.config(text="Button clicked!")

# Create the root window
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")


# Create a label widget with some text
label = tk.Label(root, text="Hello, World!")

# Create a button widget
button = tk.Button(root, text="Click me!", command=button_clicked)

# Pack the label and button widgets into the window
label.pack()
button.pack()

# Start the tkinter event loop
root.mainloop()