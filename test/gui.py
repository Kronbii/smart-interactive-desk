import tkinter as tk
import webbrowser

def openWeb():
    webbrowser.open("https://www.youtube.com/watch?v=xvFZjo5PgG0")

#main window creation
root = tk.Tk()
root.title("rami kbessne")
root.attributes("-fullscreen", True)
Label = tk.Label(root, text="khayye rami kboss el zerr promise no trolls",font=("Helvetica",40))
Label.pack(pady=20)

button = tk.Button(root, text="kbessne rami anh",command=openWeb,font=("Helvetica",30),height=3,width=15)
button.pack(pady=20)

root.mainloop()