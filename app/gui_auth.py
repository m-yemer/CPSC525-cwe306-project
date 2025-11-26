'''
Authentication dialogs - Shared between both versions
'''

def login_dialog(root, auth, set_user_label_callback, refresh_main_menu_callback):
    """Modern login dialog"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button, COLORS
    
    login_win = tk.Toplevel(root)
    login_win.title("Login")
    login_win.geometry("300x200")
    login_win.resizable(False, False)
    login_win.transient(root)
    login_win.grab_set()
    
    frame = create_modern_frame(login_win, 20)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    ttk.Label(frame, text="🔐 Login", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
    
    # Username
    ttk.Label(frame, text="Username:").pack(anchor='w')
    username_var = tk.StringVar()
    username_entry = ttk.Entry(frame, textvariable=username_var, width=25)
    username_entry.pack(fill='x', pady=(5, 15))
    username_entry.focus()
    
    # Password
    ttk.Label(frame, text="Password:").pack(anchor='w')
    password_var = tk.StringVar()
    password_entry = ttk.Entry(frame, textvariable=password_var, show="*", width=25)
    password_entry.pack(fill='x', pady=(5, 20))
    
    def perform_login():
        username = username_var.get().strip()
        password = password_var.get()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        user = auth.login_user(username, password)
        if user:
            messagebox.showinfo("Success", f"✅ Welcome back, {user['username']}!")
            login_win.destroy()
            set_user_label_callback(user)
            refresh_main_menu_callback()
        else:
            messagebox.showerror("Error", "❌ Login failed. Check your credentials.")
    
    password_entry.bind('<Return>', lambda e: perform_login())
    
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill='x', pady=(10, 0))
    
    create_modern_button(button_frame, "Login", perform_login, 'Primary.TButton').pack(side='right', padx=(5, 0))
    create_modern_button(button_frame, "Cancel", login_win.destroy, 'Secondary.TButton').pack(side='right')

def register_dialog(root, auth, CURRENT_USER, refresh_main_menu_callback):
    """Modern user registration dialog"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button
    
    reg_win = tk.Toplevel(root)
    reg_win.title("Register")
    reg_win.geometry("350x250")
    reg_win.resizable(False, False)
    
    frame = create_modern_frame(reg_win, 20)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    ttk.Label(frame, text="📝 Register New User", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
    
    # Username
    ttk.Label(frame, text="Username:").pack(anchor='w')
    username_var = tk.StringVar()
    username_entry = ttk.Entry(frame, textvariable=username_var, width=25)
    username_entry.pack(fill='x', pady=(5, 15))
    username_entry.focus()
    
    # Password
    ttk.Label(frame, text="Password:").pack(anchor='w')
    password_var = tk.StringVar()
    password_entry = ttk.Entry(frame, textvariable=password_var, show="*", width=25)
    password_entry.pack(fill='x', pady=(5, 15))
    
    # Admin checkbox
    make_admin_var = tk.BooleanVar()
    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        ttk.Checkbutton(frame, text="Make this user an admin", 
                       variable=make_admin_var).pack(anchor='w', pady=(5, 20))
    
    def perform_register():
        username = username_var.get().strip()
        password = password_var.get()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        if CURRENT_USER and CURRENT_USER.get("is_admin"):
            u = auth.register_user(username, password, is_admin=make_admin_var.get())
        else:
            u = auth.register_user(username, password)
            
        if u:
            messagebox.showinfo("Success", f"✅ User {username} registered successfully!")
            reg_win.destroy()
            refresh_main_menu_callback()
        else:
            messagebox.showerror("Error", "❌ Registration failed. Username may already exist.")
    
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill='x', pady=(10, 0))
    
    create_modern_button(button_frame, "Register", perform_register, 'Success.TButton').pack(side='right', padx=(5, 0))
    create_modern_button(button_frame, "Cancel", reg_win.destroy, 'Secondary.TButton').pack(side='right')