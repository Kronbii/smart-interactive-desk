import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from functions import load_icons, create_scrollable_page, toggle_sidebar
from functions import animate_sidebar_hide, animate_sidebar_show, create_pages
from functions import show_page, setup_header, setup_sidebar

def main():
    global root, sidebar, main_content, sidebar_visible, sidebar_width, pages
    # Set up the main application window
    root = tk.Tk()
    root.title("BEMO Smart Table")
    root.geometry("2560x1440")
    root.configure(bg="#1a1f2c")  # Elegant dark navy background
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # Sidebar state
    sidebar_visible = True
    sidebar_width = 220

    # Main content frame
    main_content = tk.Frame(root, bg="#1a1f2c", highlightbackground="red", highlightthickness=6)
    main_content.grid(row=0, column=1, sticky="nsew")
    
    # Add a thin white border to each cell in the grid
    for row in range(2):  # 2 rows: header and page content
        for col in range(1):  # 1 column
            cell = tk.Frame(main_content, bg="#1a1f2c", highlightbackground="white", highlightthickness=1)
            cell.grid(row=row, column=col, sticky="nsew")
            main_content.grid_rowconfigure(row, weight=(0 if row == 0 else 1))  # Header row has weight 0, content row has weight 1
            main_content.grid_columnconfigure(col, weight=1)

    # Sidebar frame
    sidebar = tk.Frame(root, bg="#101623", width=sidebar_width, height=650)
    sidebar.grid(row=0, column=0, sticky="ns")
    sidebar.grid_propagate(False)
    root.grid_columnconfigure(0, weight=0, minsize=sidebar_width)

    # Load icons
    icon_names = ["home", "control", "music", "stats", "list", "reminder", "alarm", "settings", "help"]
    icons = load_icons(icon_names)

    # Sidebar menu items with associated icons
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
    
    # Set up header
    setup_header(main_content, toggle_sidebar)

    # Create pages
    page_titles = ["Home", "Control", "Music", "Statistics", "Lists", "Reminders", "Alarms", "Settings", "Help & Feedback"]
    pages = create_pages(main_content, page_titles)

    # Set up sidebar
    setup_sidebar(menu_items, icons, pages, sidebar)

    # Set default page to show
    show_page("Home", pages)

    # Run the app
    root.mainloop()

if __name__ == "__main__":
    main()
