import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def invert_icon_colors(image):
    """Function to invert icon colors (black to white)."""
    image = image.convert("RGBA")
    pixels = image.load()
    
    for i in range(image.width):
        for j in range(image.height):
            r, g, b, a = pixels[i, j]
            if r == 0 and g == 0 and b == 0:  # If it's black
                pixels[i, j] = (255, 255, 255, a)  # Change to white
    return image

def load_icons(icon_names):
    """Function to load and process icons."""
    icons = {}
    for name in icon_names:
        image = Image.open(f"/home/kronbii/github-repos/smart-interactive-desk/test/gui/icons/{name}.png").resize((18, 18))
        image = invert_icon_colors(image)  # Invert the icon colors to white
        icons[name] = ImageTk.PhotoImage(image)
    return icons

def create_scrollable_page(page_frame):
    """Create a scrollable page container."""
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

def toggle_sidebar():
    """Function to toggle the visibility of the sidebar."""
    global sidebar_visible
    if sidebar_visible:
        animate_sidebar_hide()
    else:
        animate_sidebar_show()
    sidebar_visible = not sidebar_visible

def animate_sidebar_hide(root, sidebar):
    """Function to animate the hiding of the sidebar."""
    def step():
        current_width = sidebar.winfo_width()
        if current_width > 0:
            new_width = max(current_width - 20, 0)
            sidebar.config(width=new_width)
            root.grid_columnconfigure(0, minsize=new_width)
            root.after(10, step)
        else:
            sidebar.grid_remove()
            root.grid_columnconfigure(0, minsize=0)
    step()

def animate_sidebar_show(root, sidebar, sidebar_width):
    """Function to animate the showing of the sidebar."""
    sidebar.grid()
    sidebar.config(width=0)
    root.grid_columnconfigure(0, minsize=0)
    
    def step():
        current_width = sidebar.winfo_width()
        if current_width < sidebar_width:
            new_width = min(current_width + 20, sidebar_width)
            sidebar.config(width=new_width)
            root.grid_columnconfigure(0, minsize=new_width)
            root.after(10, step)
        else:
            root.grid_columnconfigure(0, minsize=sidebar_width)
    step()

def show_page(page_name, pages):
    """Function to show the selected page."""
    for page in pages.values():
        page.grid_forget()  # Hide all pages
    pages[page_name].grid(row=1, column=0, columnspan=2, sticky="nsew")  # Show the selected page

def setup_sidebar(menu_items, icons, pages, sidebar):
    """Set up the sidebar menu with buttons."""
    for item, icon_key in menu_items:
        btn = tk.Button(
            sidebar, text=f"  {item}", image=icons[icon_key], compound="left",
            anchor="w", bg="#101623", fg="white", relief="flat",
            padx=20, pady=12, font=("Segoe UI", 11), bd=0, highlightthickness=0,
            command=lambda name=item: show_page(name, pages)  # Use lambda to pass the page name
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1f2b3a"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#101623"))

def setup_header(main_content, toggle_sidebar):
    """Set up the header with the hamburger menu button and title."""
    header = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="green", highlightthickness=4)
    header.grid(row=0, column=0, sticky="new", padx=30, pady=(30, 15))
    header.columnconfigure(1, weight=1)

    hamburger_btn = tk.Button(header, text="☰", font=("Segoe UI", 16), bg="#1a1f2c", fg="white", bd=0, relief="flat", command=toggle_sidebar)
    hamburger_btn.grid(row=0, column=0, sticky="w")

    title = tk.Label(header, text="Favorites", bg="#1a1f2c", fg="white", font=("Segoe UI", 20, "bold"), anchor="w")
    title.grid(row=0, column=1, sticky="w", padx=(10, 0))

def create_pages(main_content, page_titles):
    """Create pages and populate them with sample content."""
    pages = {}

    # Make sure row 1 (page area) expands
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_columnconfigure(0, weight=1)

    for title in page_titles:
        # Create a page
        page_frame = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="pink", highlightthickness=6)
        page_frame.grid_rowconfigure(0, weight=1)
        page_frame.grid_columnconfigure(0, weight=1)

        # Inner wrapper for centering
        content_wrapper = tk.Frame(page_frame, bg="#1a1f2c")
        content_wrapper.grid(row=0, column=0, sticky="nsew")

        label = tk.Label(
            content_wrapper,
            text=f"This is the {title} page",
            fg="white",
            bg="#1a1f2c",
            font=("Segoe UI", 18)
        )
        label.pack(padx=20, pady=20)

        pages[title] = page_frame

    return pages
