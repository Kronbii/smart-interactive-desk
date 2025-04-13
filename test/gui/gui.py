import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        image = Image.open(f"/home/kronbii/github-repos/smart-interactive-desk/test/gui/icons/{name}.png").resize((24, 24))
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
    tk.Label(parent, text="Control Panel", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)
    ttk.Button(parent, text="Start").pack(pady=5)
    ttk.Button(parent, text="Stop").pack(pady=5)

def create_statistics_content(parent):
    tk.Label(parent, text="Statistics Overview", font=("Segoe UI", 18), bg="#1a1f2c", fg="white").pack(pady=20)
    tree = ttk.Treeview(parent, columns=("A", "B", "C"), show="headings", height=5)
    tree.heading("A", text="Metric")
    tree.heading("B", text="Value")
    tree.heading("C", text="Unit")
    tree.insert("", "end", values=("Speed", "120", "km/h"))
    tree.insert("", "end", values=("Power", "200", "W"))
    tree.pack()

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
        elif title == "Control":
            create_control_content(content_wrapper)
        elif title == "Statistics":
            create_statistics_content(content_wrapper)
        else:
            create_placeholder_content(content_wrapper, title)

        pages[title] = page_frame
    return pages

def main():
    global root, sidebar, main_content, sidebar_width, pages, header_title
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

    icon_names = ["home", "control", "music", "stats", "list", "reminder", "alarm", "settings", "help"]
    icons = load_icons(icon_names)

    menu_items = [
        ("Home", "home"),
        ("Control", "control"),
        ("Music", "music"),
        ("Statistics", "stats"),
        ("Lists", "list"),
        ("Reminders", "reminder"),
        ("Alarms", "alarm"),
        ("Settings", "settings"),
        ("Help & Feedback", "help")
    ]

    header_title = setup_header(main_content)
    page_titles = ["Home", "Control", "Music", "Statistics", "Lists", "Reminders", "Alarms", "Settings", "Help & Feedback"]
    pages = create_pages(main_content, page_titles)
    setup_sidebar(menu_items, icons, pages, sidebar)
    show_page("Home", pages)
    root.mainloop()

if __name__ == "__main__":
    main()
