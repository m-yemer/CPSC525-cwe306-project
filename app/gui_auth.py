'''
Professional authentication dialogs with spam protection
'''

# Track open windows to prevent multiple dialogs
_open_windows = {}

def login_dialog(root, auth_module, set_user_callback, refresh_main_callback):
    """Professional login dialog with spam protection"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button, COLORS
    from .gui_components import center_window, create_dialog_header, create_form_field
    
    # Prevent multiple login dialogs
    if 'login' in _open_windows and _open_windows['login'].winfo_exists():
        _open_windows['login'].lift()
        return
    
    login_win = tk.Toplevel(root)
    _open_windows['login'] = login_win
    login_win.title("User Login - TodoApp")
    login_win.geometry("400x300")
    login_win.resizable(False, False)
    login_win.transient(root)
    login_win.grab_set()
    
    # Configure window
    login_win.configure(bg=COLORS['background'])
    
    main_frame = create_modern_frame(login_win, 30)
    main_frame.pack(fill='both', expand=True)
    
    # Header
    create_dialog_header(main_frame, "User Login")
    
    # Form fields
    username_var, username_entry = create_form_field(main_frame, "Username:", 'entry', '', 25)
    password_var, password_entry = create_form_field(main_frame, "Password:", 'password', '', 25)
    
    # Focus username field
    username_entry.focus()
    
    # Login in progress flag
    login_in_progress = False
    
    def perform_login():
        nonlocal login_in_progress
        if login_in_progress:
            return
            
        username = username_var.get().strip()
        password = password_var.get()
        
        # Validation
        if not username:
            messagebox.showerror("Input Error", "Please enter your username.")
            username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Input Error", "Please enter your password.")
            password_entry.focus()
            return
        
        # Disable UI during login attempt
        login_in_progress = True
        login_btn.config(state='disabled')
        cancel_btn.config(state='disabled')
        
        try:
            # Authenticate user
            user = auth_module.login_user(username, password)
            if user:
                messagebox.showinfo("Login Successful", f"Welcome back, {user['username']}!")
                login_win.destroy()
                _open_windows.pop('login', None)
                set_user_callback(user)
                refresh_main_callback()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")
                password_var.set('')
                password_entry.focus()
        finally:
            # Re-enable UI
            login_in_progress = False
            login_btn.config(state='normal')
            cancel_btn.config(state='normal')
    
    def cleanup():
        """Clean up window tracking"""
        _open_windows.pop('login', None)
        login_win.destroy()
    
    # Bind Enter key to login
    password_entry.bind('<Return>', lambda e: perform_login())
    
    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=(20, 0))
    
    login_btn = create_modern_button(button_frame, "Login", perform_login, 'Primary.TButton')
    login_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = create_modern_button(button_frame, "Cancel", cleanup, 'Secondary.TButton')
    cancel_btn.pack(side='right')
    
    # Window management
    login_win.protocol("WM_DELETE_WINDOW", cleanup)
    center_window(login_win)

def register_dialog(root, auth_module, CURRENT_USER, refresh_main_callback):
    """Professional registration dialog with spam protection"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button
    from .gui_components import center_window, create_dialog_header, create_form_field
    
    # Prevent multiple registration dialogs
    if 'register' in _open_windows and _open_windows['register'].winfo_exists():
        _open_windows['register'].lift()
        return
    
    reg_win = tk.Toplevel(root)
    _open_windows['register'] = reg_win
    reg_win.title("User Registration - TodoApp")
    reg_win.geometry("450x350")
    reg_win.resizable(False, False)
    reg_win.transient(root)
    reg_win.grab_set()
    
    main_frame = create_modern_frame(reg_win, 30)
    main_frame.pack(fill='both', expand=True)
    
    # Header
    create_dialog_header(main_frame, "User Registration")
    
    # Form fields
    username_var, username_entry = create_form_field(main_frame, "Username:", 'entry', '', 25)
    password_var, password_entry = create_form_field(main_frame, "Password:", 'password', '', 25)
    
    # Admin checkbox (only for current admins)
    admin_var = None
    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        admin_var, admin_check = create_form_field(main_frame, "Grant administrator privileges", 'checkbox', False)
    
    # Focus username field
    username_entry.focus()
    
    # Registration in progress flag
    registration_in_progress = False
    
    def perform_register():
        nonlocal registration_in_progress
        if registration_in_progress:
            return
            
        username = username_var.get().strip()
        password = password_var.get()
        
        # Validation
        if not username:
            messagebox.showerror("Input Error", "Please enter a username.")
            username_entry.focus()
            return
        
        if len(username) < 3:
            messagebox.showerror("Input Error", "Username must be at least 3 characters long.")
            username_entry.focus()
            return
        
        if not password:
            messagebox.showerror("Input Error", "Please enter a password.")
            password_entry.focus()
            return
        
        if len(password) < 4:
            messagebox.showerror("Input Error", "Password must be at least 4 characters long.")
            password_entry.focus()
            return
        
        # Disable UI during registration
        registration_in_progress = True
        register_btn.config(state='disabled')
        cancel_btn.config(state='disabled')
        
        try:
            # Register user
            if CURRENT_USER and CURRENT_USER.get("is_admin") and admin_var:
                user = auth_module.register_user(username, password, is_admin=admin_var.get())
            else:
                user = auth_module.register_user(username, password)
                
            if user:
                messagebox.showinfo("Registration Successful", f"User {username} has been registered successfully!")
                reg_win.destroy()
                _open_windows.pop('register', None)
                refresh_main_callback()
            else:
                messagebox.showerror("Registration Failed", "Username already exists. Please choose a different username.")
                username_entry.focus()
        finally:
            # Re-enable UI
            registration_in_progress = False
            register_btn.config(state='normal')
            cancel_btn.config(state='normal')
    
    def cleanup():
        """Clean up window tracking"""
        _open_windows.pop('register', None)
        reg_win.destroy()
    
    # Bind Enter key to register
    password_entry.bind('<Return>', lambda e: perform_register())
    
    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=(20, 0))
    
    register_btn = create_modern_button(button_frame, "Register", perform_register, 'Success.TButton')
    register_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = create_modern_button(button_frame, "Cancel", cleanup, 'Secondary.TButton')
    cancel_btn.pack(side='right')
    
    # Window management
    reg_win.protocol("WM_DELETE_WINDOW", cleanup)
    center_window(reg_win)