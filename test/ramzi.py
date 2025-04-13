import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()
label = tk.Label(
    text="Hello, Tkinter",
    foreground="white",  # Set the text color to white
    background="black"  # Set the background color to black
)
label.pack()

window.mainloop()