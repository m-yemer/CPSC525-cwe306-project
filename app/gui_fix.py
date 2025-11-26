'''
Modernized GUI implementation with improved UI/UX - Fixed Version
'''

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from . import auth, tasks, storage, fixed, maintenance
from .gui_styles import setup_styles, create_modern_frame, create_modern_button, COLORS
from .gui_components import set_user_label, create_header, create_scrolled_text
from .gui_auth import login_dialog, register_dialog
from .gui_user_panel import open_user_panel, refresh_user_tasks_display
from .gui_admin_panel import admin_tools

# Global variables
CURRENT_USER = None
user_win = None
user_tasks_text = None
admin_win = None

def login(lbl):
    """Modern login"""
    global CURRENT_USER
    login_dialog(root, auth, 
                lambda user: set_current_user(user, lbl), 
                refresh_main_menu)

def set_current_user(user, lbl):
    """Set current user and update UI"""
    global CURRENT_USER
    CURRENT_USER = user
    set_user_label(lbl, CURRENT_USER)

def logout():
    """Logout current user"""
    global CURRENT_USER
    if not CURRENT_USER:
        return
    
    uname = CURRENT_USER.get("username")
    CURRENT_USER = None
    messagebox.showinfo("Logout", f"User {uname} logged out successfully.")
    refresh_main_menu()

def register():
    """Modern user registration"""
    register_dialog(root, auth, CURRENT_USER, refresh_main_menu)

def open_user_panel_wrapper():
    """Wrapper for user panel"""
    global user_win, user_tasks_text
    if user_win and tk.Toplevel.winfo_exists(user_win):
        user_win.lift()
        return
        
    user_win, user_tasks_text = open_user_panel(root, CURRENT_USER, tasks, refresh_user_tasks)
    refresh_user_tasks()

def refresh_user_tasks():
    """Refresh user tasks display"""
    global user_tasks_text
    if user_tasks_text:
        refresh_user_tasks_display(user_tasks_text, CURRENT_USER, tasks, COLORS)

def admin_tools_wrapper():
    """Wrapper for admin tools"""
    global admin_win
    admin_win = admin_tools(root, CURRENT_USER, auth, fixed, storage, maintenance, refresh_main_menu)

def quit_app():
    """Gracefully quit the application"""
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        root.destroy()

def refresh_main_menu():
    """Refresh the main menu with current user state"""
    # Clear existing widgets except user label
    for widget in main_frame.winfo_children():
        if widget != user_lbl:
            widget.destroy()
    
    set_user_label(user_lbl, CURRENT_USER)
    
    # Create modern button grid
    button_frame = create_modern_frame(main_frame, 20)
    button_frame.pack(fill='both', expand=True, pady=20)
    
    # Row 1: Login/Logout and Register
    if not CURRENT_USER:
        create_modern_button(button_frame, "Login", 
                            lambda: [login(user_lbl)], 
                            'Primary.TButton', 18).grid(row=0, column=0, padx=10, pady=10)
    else:
        create_modern_button(button_frame, "Logout", 
                            lambda: [logout()], 
                            'Secondary.TButton', 18).grid(row=0, column=0, padx=10, pady=10)
    
    create_modern_button(button_frame, "Register", 
                        lambda: [register()], 
                        'Success.TButton', 18).grid(row=0, column=1, padx=10, pady=10)
    
    # Row 2: App and Admin Tools
    create_modern_button(button_frame, "Use App", 
                        open_user_panel_wrapper, 
                        'Primary.TButton', 18).grid(row=1, column=0, padx=10, pady=10)
    
    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        create_modern_button(button_frame, "Admin Tools", 
                            admin_tools_wrapper, 
                            'Warning.TButton', 18).grid(row=1, column=1, padx=10, pady=10)
    else:
        # Placeholder to maintain grid layout
        ttk.Frame(button_frame, width=1, height=1).grid(row=1, column=1, padx=10, pady=10)
    
    # Row 3: Quit button
    create_modern_button(button_frame, "Quit", 
                        quit_app, 
                        'Danger.TButton', 38).grid(row=2, column=0, columnspan=2, pady=20, sticky='ew')

if __name__ == "__main__":
    # Initialize the main application
    root = tk.Tk()
    root.title("TodoApp - Fixed GUI")
    root.geometry("500x400")
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    # Setup modern styles
    setup_styles()
    
    # Main container
    main_container = create_modern_frame(root, 0)
    main_container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # App header
    header_frame = create_header(main_container, "TodoApp - Fixed GUI", 
                               "Secure • Modern • Efficient")
    
    # User info
    user_frame = create_modern_frame(main_container, 15)
    user_frame.pack(fill='x', pady=(0, 20))
    
    user_lbl = ttk.Label(user_frame, text="User: Not logged in", 
                        font=('Arial', 12))
    user_lbl.pack(anchor='w')
    
    # Main menu frame
    main_frame = create_modern_frame(main_container, 0)
    main_frame.pack(fill='both', expand=True)
    
    # Initialize the interface
    refresh_main_menu()
    
    # Start the application
    root.mainloop()