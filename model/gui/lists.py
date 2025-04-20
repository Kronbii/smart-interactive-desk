import tkinter as tk
from tkinter import ttk
from box import Box
import yaml
from gui import CONFIG_PATH

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

def create_list_content(parent):
    # Main container frame
    task_frame = tk.Frame(parent, bg=config.theme.background_color)
    task_frame.pack(pady=20, fill="both", expand=True)

    # Input for new task — Entry + Button (TOP)
    task_entry_frame = tk.Frame(task_frame, bg=config.theme.background_color)
    task_entry_frame.pack(fill="x", pady=(0, 10))

    task_entry = tk.Entry(task_entry_frame, font=(config.theme.font_family, 12), bg=config.theme.task_entry_color, fg="white", insertbackground="white")
    task_entry.pack(side="left", padx=(10, 5), fill="x", expand=True)

    add_task_btn = tk.Button(task_entry_frame, text="Add Task", font=(config.theme.font_family, 12, "bold"),
                             bg=config.theme.add_task_color, fg="white", command=lambda: add_task())
    add_task_btn.pack(side="right", padx=(5, 10))

    # Scrollable canvas for tasks
    canvas_frame = tk.Frame(task_frame, bg=config.theme.background_color)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg=config.theme.background_color, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas to hold all tasks
    task_list_frame = tk.Frame(canvas, bg=config.theme.background_color)
    task_window = canvas.create_window((0, 0), window=task_list_frame, anchor="nw")

    # Allow resizing and scrolling
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(task_window, width=event.width)

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    task_list_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)
    canvas.bind_all("<MouseWheel>", on_mousewheel)  # enable scrolling with mousewheel

    tasks = []

    def on_checkbox_toggle(task_name, var, task_box):
        if var.get():
            tasks.remove(task_name)
            task_box.destroy()
            refresh_task_list()

    def add_task():
        new_task = task_entry.get()
        if new_task.strip():
            tasks.append(new_task.strip())
            task_entry.delete(0, tk.END)
            refresh_task_list()

    def refresh_task_list():
        for widget in task_list_frame.winfo_children():
            widget.destroy()
        create_task_list()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def create_task_list():
        for task in tasks:
            task_box = tk.Frame(task_list_frame, bg=config.theme.taskbox_color, pady=10, padx=15, relief="solid", borderwidth=1)
            task_box.pack(fill="x", pady=5, padx=10)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                task_box, variable=var, bg=config.theme.taskbox_color, fg="white",
                selectcolor=config.theme.font_color, activebackground=config.theme.taskbox_color,
                command=lambda t=task, v=var, box=task_box: on_checkbox_toggle(t, v, box),
                font=(config.theme.font_family, 12), width=2
            )
            checkbox.pack(side="left", padx=10)

            label = tk.Label(task_box, text=task, bg=config.theme.taskbox_color, fg="white", font=(config.theme.font_family, 12))
            label.pack(side="left", padx=10)

    # Optional: preload example tasks
    tasks.extend(["Example Task 1", "Example Task 2"])
    refresh_task_list()

    # 👉 Allow pressing Enter to add tasks
    task_entry.bind("<Return>", lambda event: add_task())