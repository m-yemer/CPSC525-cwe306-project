'''
Modernized GUI implementation with improved UI/UX - Fixed Version
'''

import tkinter as tk
from tkinter import ttk, messagebox
from . import auth, tasks, storage, fixed, maintenance
from .gui_styles import setup_styles, create_modern_frame, create_modern_button, COLORS
from .gui_components import set_user_label, create_header, center_window
from .gui_auth import login_dialog, register_dialog
from .gui_user_panel import open_user_panel, refresh_user_tasks_display
from .gui_admin_panel import admin_tools

# Global variables
CURRENT_USER = None
user_win = None
user_tasks_text = None
admin_win = None

# Window management
_open_windows = {}

def login(lbl):
    """Professional login handler"""
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
    """Professional logout handler"""
    global CURRENT_USER, user_win, admin_win
    
    if not CURRENT_USER:
        return
    
    # Confirm logout
    if not messagebox.askyesno("Confirm Logout", 
                              f"Are you sure you want to log out {CURRENT_USER['username']}?"):
        return
    
    # Close open windows
    if user_win and user_win.winfo_exists():
        user_win.destroy()
        user_win = None
    
    if admin_win and admin_win.winfo_exists():
        admin_win.destroy()
        admin_win = None
    
    # Clear user data
    username = CURRENT_USER.get("username")
    CURRENT_USER = None
    
    messagebox.showinfo("Logout Successful", f"User {username} has been logged out.")
    refresh_main_menu()

def register():
    """Professional registration handler"""
    register_dialog(root, auth, CURRENT_USER, refresh_main_menu)

def open_user_panel_wrapper():
    """Professional user panel wrapper"""
    global user_win, user_tasks_text
    
    # Check authentication
    if not CURRENT_USER:
        messagebox.showwarning("Authentication Required", 
                              "Please log in to access the Task Manager.")
        return
    
    # Manage window instance
    if user_win and user_win.winfo_exists():
        user_win.lift()
        user_win.focus_set()
        return
    
    # Open new user panel
    user_win, user_tasks_text = open_user_panel(root, CURRENT_USER, tasks, refresh_user_tasks)
    
    # Track window for cleanup
    if user_win:
        def on_user_win_close():
            global user_win, user_tasks_text
            user_win = None
            user_tasks_text = None
            user_win_closed()
        
        user_win.protocol("WM_DELETE_WINDOW", on_user_win_close)

def refresh_user_tasks():
    """Refresh user tasks display"""
    global user_tasks_text
    if user_tasks_text and hasattr(user_tasks_text, 'winfo_exists') and user_tasks_text.winfo_exists():
        refresh_user_tasks_display(user_tasks_text, CURRENT_USER, tasks, COLORS)

def user_win_closed():
    """Handle user window closure"""
    global user_win, user_tasks_text
    user_win = None
    user_tasks_text = None

def admin_tools_wrapper():
    """Professional admin tools wrapper"""
    global admin_win
    
    # Check admin privileges
    if not CURRENT_USER or not CURRENT_USER.get("is_admin"):
        # Allow admin authentication even if not logged in as admin
        if not messagebox.askyesno("Admin Access", 
                                  "Administrator privileges are required.\n\n"
                                  "Do you want to authenticate as an administrator?"):
            return
    
    # Manage window instance
    if admin_win and admin_win.winfo_exists():
        admin_win.lift()
        admin_win.focus_set()
        return
    
    # Open admin tools
    admin_win = admin_tools(root, CURRENT_USER, auth, fixed, storage, maintenance, refresh_main_menu)
    
    # Track window for cleanup
    if admin_win:
        def on_admin_win_close():
            global admin_win
            admin_win = None
            admin_win_closed()
        
        admin_win.protocol("WM_DELETE_WINDOW", on_admin_win_close)

def admin_win_closed():
    """Handle admin window closure"""
    global admin_win
    admin_win = None

def quit_app():
    """Professional application quit handler"""
    # Check for unsaved work (optional - could be enhanced)
    unsaved_changes = False
    
    if unsaved_changes:
        response = messagebox.askyesnocancel(
            "Unsaved Changes",
            "You have unsaved changes. Would you like to save before quitting?",
            icon='warning'
        )
        
        if response is None:  # Cancel
            return
        elif response:  # Yes - save changes
            # Implement save logic here if needed
            pass
    
    # Confirm quit
    if messagebox.askokcancel("Quit Application", 
                             "Are you sure you want to quit TodoApp?"):
        # Clean up resources
        global user_win, admin_win
        
        if user_win and user_win.winfo_exists():
            user_win.destroy()
        
        if admin_win and admin_win.winfo_exists():
            admin_win.destroy()
        
        root.destroy()

def refresh_main_menu():
    """Refresh the main menu with current user state"""
    global main_frame, user_lbl
    
    # Clear existing widgets except user label
    for widget in main_frame.winfo_children():
        if widget != user_lbl:
            widget.destroy()
    
    # Update user label
    set_user_label(user_lbl, CURRENT_USER)
    
    # Create centered main menu
    menu_container = create_modern_frame(main_frame, 0)
    menu_container.pack(expand=True, fill='both', pady=20)
    
    # Menu frame with fixed width for better centering
    menu_frame = create_modern_frame(menu_container, 30)
    menu_frame.pack(expand=True)
    
    # Welcome message for logged-in users
    if CURRENT_USER:
        welcome_frame = create_modern_frame(menu_frame, 15)
        welcome_frame.pack(fill='x', pady=(0, 20))
        
        welcome_text = f"Welcome back, {CURRENT_USER['username']}!"
        if CURRENT_USER.get('is_admin'):
            welcome_text += " (Administrator)"
        
        ttk.Label(welcome_frame, text=welcome_text, 
                 style='Header.TLabel').pack(anchor='center')
    
    # Button grid container
    button_grid = create_modern_frame(menu_frame, 0)
    button_grid.pack(expand=True)
    
    # Row 1: Authentication buttons
    auth_frame = create_modern_frame(button_grid, 10)
    auth_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=10)
    
    if not CURRENT_USER:
        # Login button
        login_btn = create_modern_button(auth_frame, "Login", 
                                      lambda: login(user_lbl), 
                                      'Primary.TButton', 18)
        login_btn.pack(side='left', padx=(0, 10), expand=True, fill='x')
        
        # Register button
        register_btn = create_modern_button(auth_frame, "Register", 
                                         lambda: register(), 
                                         'Success.TButton', 18)
        register_btn.pack(side='left', expand=True, fill='x')
    else:
        # Logout button
        logout_btn = create_modern_button(auth_frame, "Logout", 
                                       lambda: logout(), 
                                       'Secondary.TButton', 18)
        logout_btn.pack(side='left', padx=(0, 10), expand=True, fill='x')
        
        # User info (static)
        user_info_btn = create_modern_button(auth_frame, f"User: {CURRENT_USER['username']}", 
                                          lambda: None, 
                                          'Secondary.TButton', 18)
        user_info_btn.pack(side='left', expand=True, fill='x')
        user_info_btn.config(state='disabled')  # Make it look like a label
    
    # Row 2: Application buttons
    app_frame = create_modern_frame(button_grid, 10)
    app_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=10)
    
    # Use Application button (always visible)
    use_app_btn = create_modern_button(app_frame, "Task Manager", 
                                    open_user_panel_wrapper, 
                                    'Primary.TButton', 18)
    use_app_btn.pack(side='left', padx=(0, 10), expand=True, fill='x')
    
    # Admin Tools button (conditional)
    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        admin_btn = create_modern_button(app_frame, "Admin Tools", 
                                      admin_tools_wrapper, 
                                      'Warning.TButton', 18)
        admin_btn.pack(side='left', expand=True, fill='x')
    else:
        # Placeholder to maintain layout
        placeholder = create_modern_button(app_frame, "Admin Tools", 
                                        lambda: admin_tools_wrapper(), 
                                        'Secondary.TButton', 18)
        placeholder.pack(side='left', expand=True, fill='x')
        placeholder.config(state='disabled')
    
    # Row 3: System buttons
    system_frame = create_modern_frame(button_grid, 10)
    system_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=10)
    
    # Quit button (full width)
    quit_btn = create_modern_button(system_frame, "Quit Application", 
                                 quit_app, 
                                 'Danger.TButton', 36)
    quit_btn.pack(fill='x')
    
    # Application info footer
    footer_frame = create_modern_frame(menu_frame, 15)
    footer_frame.pack(fill='x', pady=(30, 0))
    
    ttk.Label(footer_frame, text="TodoApp - Secure Task Management System", 
             style='Subtitle.TLabel').pack(anchor='center')
    ttk.Label(footer_frame, text="Fixed Version - CWE-306 Demonstration", 
             style='Subtitle.TLabel').pack(anchor='center')

def initialize_application():
    """Initialize the main application window"""
    global root, main_container, main_frame, user_lbl
    
    # Create main window
    root = tk.Tk()
    root.title("TodoApp - Fixed GUI")
    root.geometry("700x550")
    root.minsize(600, 450)
    
    # Set window icon (optional)
    try:
        root.iconbitmap('')  # Could set an icon file here
    except:
        pass  # Use default icon
    
    # Configure window
    root.configure(bg=COLORS['background'])
    
    # Setup professional styles
    setup_styles()
    
    # Main container with proper padding
    main_container = create_modern_frame(root, 0)
    main_container.pack(fill='both', expand=True, padx=40, pady=30)
    
    # Application header
    header_frame = create_header(main_container, 
                               "TodoApp - Fixed GUI", 
                               "Professional Task Management System")
    
    # User status section
    user_section = create_modern_frame(main_container, 15)
    user_section.pack(fill='x', pady=(0, 30))
    
    ttk.Label(user_section, text="Current Session", 
             style='Header.TLabel').pack(anchor='w', pady=(0, 8))
    
    # User label with initial state
    user_lbl = ttk.Label(user_section, text="User: Not logged in", 
                        font=('Arial', 11))
    user_lbl.pack(anchor='w')
    
    # Main menu area (centered)
    main_frame = create_modern_frame(main_container, 0)
    main_frame.pack(fill='both', expand=True)
    
    # Initialize menu
    refresh_main_menu()
    
    # Center window on screen
    center_window(root)
    
    # Set focus to main window
    root.focus_set()
    
    return root

if __name__ == "__main__":
    # Initialize and start the application
    app = initialize_application()
    
    # Start the main event loop
    try:
        app.mainloop()
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        print("\nApplication terminated by user.")
    except Exception as e:
        # Handle unexpected errors
        messagebox.showerror("Application Error", 
                           f"An unexpected error occurred:\n\n{str(e)}")
        print(f"Application error: {e}")