import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def send_command(command):
    # Placeholder function for sending commands
    print(f"Command sent: {command}")

def invert_icon_colors(image):
    image = image.convert("RGBA")
    pixels = image.load()
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if r == 0 and g == 0 and b == 0:
                pixels[i, j] = (255, 255, 255, a)
    return image

def load_icons(icon_names):
    icons = {}
    for name in icon_names:
        image_path = os.path.join(os.path.dirname(__file__), "icons", f"{name}.png")
        image = Image.open(image_path).resize((24, 24))
        image = invert_icon_colors(image)
        icons[name] = ImageTk.PhotoImage(image)
    return icons

def create_scrollable_page(page_frame):
    canvas = tk.Canvas(page_frame, bg="#1a1f2c")
    scroll_y = tk.Scrollbar(page_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    page_container = tk.Frame(canvas, bg="#1a1f2c")
    canvas.create_window((0, 0), window=page_container, anchor="nw")
    page_container.grid_rowconfigure(0, weight=1)
    page_container.grid_columnconfigure(0, weight=1)
    return page_container

def show_page(page_name, pages):
    for page in pages.values():
        page.grid_forget()
    pages[page_name].grid(row=1, column=0, columnspan=2, sticky="nsew")
    header_title.config(text=page_name)

def setup_sidebar(menu_items, icons, pages, sidebar):
    for item, icon_key in menu_items:
        btn = tk.Button(
            sidebar, text=f"  {item}", image=icons[icon_key], compound="left",
            anchor="w", bg="#101623", fg="white", relief="flat",
            padx=20, pady=17, font=("Segoe UI", 11), bd=0, highlightthickness=0,
            command=lambda name=item: show_page(name, pages)
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1f2b3a"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#101623"))

def setup_header(main_content):
    header = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="green", highlightthickness=4)
    header.grid(row=0, column=0, sticky="new", padx=30, pady=(30, 15))
    header.columnconfigure(1, weight=1)
    title = tk.Label(header, text="", bg="#1a1f2c", fg="white", font=("Segoe UI", 20, "bold"), anchor="w")
    title.grid(row=0, column=1, sticky="w", padx=(10, 0))
    return title

def create_home_content(parent):
    tk.Label(parent, text="Welcome to Home Page", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)
    tk.Button(parent, text="Click Me", bg="#2e3a59", fg="white").pack()

def create_control_content(parent):
    style = ttk.Style()
    
    # Set theme engine to support styling (important for Linux)
    style.theme_use("clam")

    # Base style
    style.configure(
        "Base.TButton",
        font=("Segoe UI", 12, "bold"),
        padding=(25, 15), 
        foreground="#ffffff",
        background="#2e3a59",
        borderwidth=0,
        relief="flat",
        focuscolor="none"
    )
    style.map(
        "Base.TButton",
        background=[("active", "#3e4a6d")],
        foreground=[("active", "#ffffff")]
    )

    # Rounded buttons via element create hack (on some systems)
    style.layout("Rounded.TButton", [
        ("Button.border", {"children": [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})]})], "sticky": "nswe"})
    ])
    style.configure("Rounded.TButton", borderwidth=5, relief="flat", background="#2e3a59", padding=(25, 15), foreground="white", font=("Segoe UI", 12, "bold"))
    style.map("Rounded.TButton", background=[("active", "#3e4a6d")])

    # Outer frame for padding
    frame = tk.Frame(parent, bg="#1a1f2c")
    frame.pack(pady=40)

    def on_button_release():
        send_command("stop")
    
    # Buttons with hierarchy and layout
    up_btn = ttk.Button(frame, text="↑ Up", style="Rounded.TButton")
    down_btn = ttk.Button(frame, text="↓ Down", style="Rounded.TButton")
    tilt_up_btn = ttk.Button(frame, text="↥ Tilt Up", style="Rounded.TButton")
    tilt_down_btn = ttk.Button(frame, text="↧ Tilt Down", style="Rounded.TButton")
    stop_btn = ttk.Button(frame, text="■ Stop", style="Rounded.TButton", command=lambda: send_command("stop"))  # visually prioritized

    # Bind button press and release events to each button
    up_btn.bind("<ButtonPress-1>", lambda e: send_command("up"))
    up_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())
    
    down_btn.bind("<ButtonPress-1>", lambda e: send_command("down"))
    down_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())
    
    tilt_up_btn.bind("<ButtonPress-1>", lambda e: send_command("tilt up"))
    tilt_up_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())
    
    tilt_down_btn.bind("<ButtonPress-1>", lambda e: send_command("tilt down"))
    tilt_down_btn.bind("<ButtonRelease-1>", lambda e: on_button_release())
    
    # Grid layout
    up_btn.grid(row=0, column=0, padx=15, pady=15)
    down_btn.grid(row=0, column=1, padx=15, pady=15)
    tilt_up_btn.grid(row=1, column=0, padx=15, pady=15)
    tilt_down_btn.grid(row=1, column=1, padx=15, pady=15)
    stop_btn.grid(row=2, column=0, padx=15, pady=15)


def create_statistics_content(parent):
    tk.Label(parent, text="Statistics Overview", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)
    tree = ttk.Treeview(parent, columns=("A", "B", "C"), show="headings", height=5)
    tree.heading("A", text="Metric")
    tree.heading("B", text="Value")
    tree.heading("C", text="Unit")
    tree.insert("", "end", values=("Speed", "120", "km/h"))
    tree.insert("", "end", values=("Power", "200", "W"))
    tree.pack()
    
def create_list_content(parent):
    # Frame to hold the task list
    task_frame = tk.Frame(parent, bg="#1a1f2c")
    task_frame.pack(pady=20, fill="both", expand=True)

    # Scrollable Canvas and Scrollbar
    canvas = tk.Canvas(task_frame, bg="#1a1f2c")
    scrollbar = tk.Scrollbar(task_frame, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame inside canvas to hold tasks
    task_list_frame = tk.Frame(canvas, bg="#1a1f2c")
    canvas.create_window((0, 0), window=task_list_frame, anchor="nw")

    task_list_frame.grid_rowconfigure(0, weight=1)
    task_list_frame.grid_columnconfigure(0, weight=1)

    # List of tasks (initialized with some tasks)
    tasks = [
        "Task 1: Check the system status",
        "Task 2: Update the software",
        "Task 3: Run diagnostics",
        "Task 4: Restart the system",
        "Task 5: Backup the data"
    ]
    
    def on_checkbox_toggle(task_name, var, task_box):
        if var.get():  # If checkbox is checked, delete the task
            tasks.remove(task_name)
            task_box.destroy()  # Remove task from display
            refresh_task_list()

    def add_task():
        new_task = task_entry.get()
        if new_task:  # Ensure the task is not empty
            tasks.append(new_task)
            task_entry.delete(0, tk.END)  # Clear the input box
            refresh_task_list()

    def refresh_task_list():
        # Clear the task frame and re-create the tasks
        for widget in task_list_frame.winfo_children():
            widget.destroy()
        create_task_list()
        # Update the scroll region based on the content size
        canvas.config(scrollregion=canvas.bbox("all"))

    def create_task_list():
        # Create each task with a checkbox
        for task in tasks:
            task_box = tk.Frame(task_list_frame, bg="#2e3a59", pady=10, padx=15, relief="solid", borderwidth=1)
            task_box.pack(fill="x", pady=5)

            # Checkbox variable to track task state
            var = tk.BooleanVar()
            
            # Create the checkbox and task label
            checkbox = tk.Checkbutton(task_box, variable=var, bg="#2e3a59", fg="white", selectcolor="#3e4a6d", activebackground="#2e4a69", command=lambda t=task, v=var, box=task_box: on_checkbox_toggle(t, v, box), height=2, width=2)
            checkbox.pack(side="left", padx=10)
            
            label = tk.Label(task_box, text=task, bg="#2e3a59", fg="white", font=("Segoe UI", 12))
            label.pack(side="left", padx=10)

    # Input for new task
    task_entry_frame = tk.Frame(task_frame, bg="#1a1f2c")
    task_entry_frame.pack(fill="x", pady=10)
    
    task_entry = tk.Entry(task_entry_frame, font=("Segoe UI", 12), bg="#3e4a6d", fg="white", insertbackground="white")
    task_entry.pack(side="left", padx=10, fill="x", expand=True)
    
    add_task_btn = tk.Button(task_entry_frame, text="Add Task", font=("Segoe UI", 12, "bold"), bg="#2e3a59", fg="white", command=add_task)
    add_task_btn.pack(side="right", padx=10)

    # Create initial list of tasks
    create_task_list()
    # Update the scroll region when tasks are loaded
    canvas.config(scrollregion=canvas.bbox("all"))




def create_placeholder_content(parent, title):
    tk.Label(parent, text=f"This is the {title} page", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)

def create_pages(main_content, page_titles):
    pages = {}
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_columnconfigure(0, weight=1)
    for title in page_titles:
        page_frame = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="pink", highlightthickness=6)
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)
        content_wrapper = tk.Frame(page_frame, bg="#1a1f2c")
        content_wrapper.grid(row=0, column=0, sticky="nsew")

        if title == "Home":
            create_home_content(content_wrapper)
        elif title == "Control Panel":
            create_control_content(content_wrapper)
        elif title == "Statistics":
            create_statistics_content(content_wrapper)
        elif title == "Lists":
            create_list_content(content_wrapper)
        else:
            create_placeholder_content(content_wrapper, title)

        pages[title] = page_frame
    return pages

def main():
    global root, sidebar, main_content, sidebar_width, pages, header_title
    
    icon_names = ["home", "control", "music", "stats", "list", "reminder", "alarm", "settings", "help"]
    page_titles = ["Home", "Control Panel", "Music", "Statistics", "Lists", "Reminders", "Alarms", "Settings", "Help & Feedback"]
    menu_items = [
    (page_titles[0], "home"),
    (page_titles[1], "control"),
    (page_titles[2], "music"),
    (page_titles[3], "stats"),
    (page_titles[4], "list"),
    (page_titles[5], "reminder"),
    (page_titles[6], "alarm"),
    (page_titles[7], "settings"),
    (page_titles[8], "help")
]
    
    root = tk.Tk()
    root.title("BEMO Smart Table")
    root.geometry("2560x1440")
    root.configure(bg="#1a1f2c")
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    sidebar_width = 220

    main_content = tk.Frame(root, bg="#1a1f2c", highlightbackground="red", highlightthickness=6)
    main_content.grid(row=0, column=1, sticky="nsew")
    for row in range(2):
        for col in range(1):
            cell = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="white", highlightthickness=1)
            cell.grid(row=row, column=col, sticky="nsew")
            main_content.grid_rowconfigure(row, weight=(0 if row == 0 else 1))
            main_content.grid_columnconfigure(col, weight=1)

    sidebar = tk.Frame(root, bg="#101623", width=sidebar_width, height=650)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

    icons = load_icons(icon_names)

    header_title = setup_header(main_content)
    pages = create_pages(main_content, page_titles)
    setup_sidebar(menu_items, icons, pages, sidebar)
    show_page("Control Panel", pages)
    root.mainloop()

if __name__ == "__main__":
    main()
