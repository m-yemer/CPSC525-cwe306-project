'''
Vulnerable GUI implementation - Comprehensive CWE-306 demonstration
'''

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from . import auth, tasks, storage, vulnerable, maintenance
from .gui_styles import setup_styles, create_modern_frame, create_modern_button, COLORS
from .gui_components import set_user_label, create_header, center_window, create_scrolled_text

# Global variables
CURRENT_USER = None
user_win = None
user_tasks_text = None
admin_win = None

def login(lbl):
    """Vulnerable login - No proper session management"""
    global CURRENT_USER
    username = simpledialog.askstring("Login", "Username:")
    if not username:
        return
    
    password = simpledialog.askstring("Login", "Password:", show="*")
    user = auth.login_user(username, password)
    
    if user:
        CURRENT_USER = user
        # VULNERABLE: No proper session validation
        set_user_label(lbl, CURRENT_USER)
        messagebox.showinfo("Login", f"Logged in as {user['username']}")
        refresh_main_menu()
    else:
        messagebox.showerror("Login", "Login failed")

def logout():
    """Vulnerable logout - No session cleanup"""
    global CURRENT_USER
    if not CURRENT_USER:
        return
    
    uname = CURRENT_USER.get("username")
    CURRENT_USER = None
    messagebox.showinfo("Logout", f"User {uname} logged out.")
    refresh_main_menu()

def register():
    """Vulnerable registration - No input validation"""
    username = simpledialog.askstring("Register", "Choose username:")
    if not username:
        return
    
    password = simpledialog.askstring("Register", "Choose password:", show="*")
    
    # VULNERABLE: Any user can create admin accounts
    if CURRENT_USER:
        make_admin = messagebox.askyesno("Register", "Make this user admin?")
        u = auth.register_user(username, password, is_admin=make_admin)
    else:
        u = auth.register_user(username, password)
    
    if u:
        messagebox.showinfo("Register", f"Registered {username}")
    else:
        messagebox.showerror("Register", "Registration failed")

def open_user_panel():
    """Vulnerable user panel - No access control"""
    global user_win, user_tasks_text
    
    if user_win and tk.Toplevel.winfo_exists(user_win):
        user_win.lift()
        return
    
    user_win = tk.Toplevel(root)
    user_win.title("Task Manager - VULNERABLE")
    user_win.geometry("800x600")
    
    # VULNERABLE: No authentication check
    header_frame = create_header(user_win, "Task Manager - VULNERABLE", 
                               "No proper access control")
    
    # Action buttons
    button_frame = create_modern_frame(user_win, 10)
    button_frame.pack(fill='x', padx=20, pady=(0, 10))
    
    create_modern_button(button_frame, "Create Task", create_task, 'Success.TButton', 15).grid(row=0, column=0, padx=5, pady=5)
    create_modern_button(button_frame, "Complete Task", complete_task, 'Primary.TButton', 15).grid(row=0, column=1, padx=5, pady=5)
    create_modern_button(button_frame, "Delete Task", delete_task, 'Danger.TButton', 15).grid(row=0, column=2, padx=5, pady=5)
    create_modern_button(button_frame, "View ALL Tasks", view_all_tasks, 'Warning.TButton', 15).grid(row=0, column=3, padx=5, pady=5)
    
    # Tasks display
    tasks_frame = create_modern_frame(user_win, 10)
    tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    ttk.Label(tasks_frame, text="Task Display:", font=('Arial', 12, 'bold')).pack(anchor='w')
    
    user_tasks_text = create_scrolled_text(tasks_frame)
    user_tasks_text.pack(fill='both', expand=True, pady=(10, 0))
    
    refresh_user_tasks()

def refresh_user_tasks():
    """Vulnerable task refresh - Shows all tasks to everyone"""
    global user_tasks_text
    if not user_tasks_text:
        return
        
    user_tasks_text.config(state=tk.NORMAL)
    user_tasks_text.delete("1.0", tk.END)
    
    # VULNERABLE: Shows all tasks regardless of ownership
    all_tasks = storage.load_tasks() or []
    
    if not all_tasks:
        user_tasks_text.insert(tk.END, "No tasks in system\n")
    else:
        user_tasks_text.insert(tk.END, "VULNERABLE: Viewing ALL tasks in system\n\n")
        for t in all_tasks:
            status = "DONE" if t.get("done") else "PENDING"
            user_tasks_text.insert(tk.END, f"[{status}] Task #{t['id']} (Owner: {t['owner_id']}): {t['title']}\n")
            if t.get('description'):
                user_tasks_text.insert(tk.END, f"    Desc: {t['description']}\n")
            user_tasks_text.insert(tk.END, f"    Created: {t['created_at']}\n\n")
    
    user_tasks_text.config(state=tk.DISABLED)

def create_task():
    """Vulnerable task creation - No user validation"""
    if not CURRENT_USER:
        # VULNERABLE: Allows task creation without login
        owner_id = simpledialog.askinteger("Create Task", "Enter any user ID to own this task:")
        if owner_id is None:
            return
    else:
        owner_id = CURRENT_USER["id"]
    
    title = simpledialog.askstring("Create Task", "Title:")
    if title is None:
        return
    
    desc = simpledialog.askstring("Create Task", "Description:")
    t = tasks.add_task(owner_id, title, desc or "")
    
    messagebox.showinfo("Create", f"Created task id={t['id']} for user {owner_id}")
    refresh_user_tasks()

def complete_task():
    """Vulnerable task completion - No ownership check"""
    tid = simpledialog.askinteger("Complete Task", "Task id to mark complete:")
    if tid is None:
        return
    
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Complete", "Task not found")
        return
    
    # VULNERABLE: No ownership validation
    tasks.update_task(tid, done=True)
    messagebox.showinfo("Complete", f"Task {tid} marked complete")
    refresh_user_tasks()

def delete_task():
    """Vulnerable task deletion - No authorization"""
    tid = simpledialog.askinteger("Delete Task", "Task id to delete:")
    if tid is None:
        return
    
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Delete", "Task not found")
        return
    
    # VULNERABLE: No ownership check
    tasks.delete_task(tid)
    messagebox.showinfo("Delete", f"Task {tid} deleted")
    refresh_user_tasks()

def view_all_tasks():
    """Vulnerable: Explicitly show all tasks to any user"""
    all_tasks = storage.load_tasks() or []
    all_users = storage.load_users() or []
    
    view_win = tk.Toplevel(root)
    view_win.title("ALL SYSTEM DATA - VULNERABLE")
    view_win.geometry("900x700")
    
    text_area = scrolledtext.ScrolledText(view_win, width=100, height=35)
    text_area.pack(fill='both', expand=True, padx=20, pady=20)
    
    content = "SECURITY VULNERABILITY: All System Data Exposed\n"
    content += "=" * 60 + "\n\n"
    
    # Show all users
    content += "ALL USERS:\n"
    content += "-" * 30 + "\n"
    for user in all_users:
        content += f"ID: {user['id']} | Username: {user['username']} | Admin: {user.get('is_admin', False)}\n"
    content += "\n"
    
    # Show all tasks
    content += "ALL TASKS:\n"
    content += "-" * 30 + "\n"
    for task in all_tasks:
        content += f"Task ID: {task['id']} | Owner: {task['owner_id']} | Title: {task['title']}\n"
        if task.get('description'):
            content += f"    Description: {task['description']}\n"
        content += f"    Status: {'COMPLETED' if task.get('done') else 'PENDING'} | Created: {task['created_at']}\n\n"
    
    text_area.insert('1.0', content)
    text_area.config(state='disabled')
    
    center_window(view_win)

def admin_tools():
    """Vulnerable admin tools - No authentication required"""
    global admin_win
    
    if admin_win and tk.Toplevel.winfo_exists(admin_win):
        admin_win.lift()
        return
    
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Tools - VULNERABLE")
    admin_win.geometry("600x500")
    
    # VULNERABLE: No authentication check
    header_frame = create_header(admin_win, "Admin Tools - VULNERABLE", 
                               "NO AUTHENTICATION REQUIRED - CWE-306")
    
    # Security warning
    warning_frame = create_modern_frame(admin_win, 15)
    warning_frame.pack(fill='x', padx=40, pady=(0, 20))
    
    ttk.Label(warning_frame, text="⚠️  SECURITY VULNERABILITY", 
             foreground='red', font=('Arial', 12, 'bold')).pack()
    ttk.Label(warning_frame, text="Admin functions accessible without authentication", 
             foreground='red', font=('Arial', 10)).pack()
    
    # Admin operations
    content_frame = create_modern_frame(admin_win, 30)
    content_frame.pack(fill='both', expand=True, padx=40, pady=20)
    
    create_modern_button(content_frame, "Delete ALL Tasks", 
                       vulnerable_delete_all, 
                       'Danger.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(content_frame, "View All User Data", 
                       view_all_user_data, 
                       'Warning.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(content_frame, "System Maintenance", 
                       vulnerable_maintenance, 
                       'Primary.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(content_frame, "Create Admin User", 
                       create_admin_user, 
                       'Success.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(content_frame, "Close", 
                       admin_win.destroy, 
                       'Secondary.TButton', 25).pack(fill='x', pady=8)
    
    center_window(admin_win)

def vulnerable_delete_all():
    """Vulnerable: Delete all tasks without authentication"""
    if messagebox.askyesno("Delete All", 
                          "VULNERABLE: This will delete ALL tasks without authentication!\n\n"
                          "Continue?"):
        vulnerable.delete_all_tasks()
        messagebox.showinfo("Success", "All tasks deleted (VULNERABLE)")
        refresh_user_tasks()

def view_all_user_data():
    """Vulnerable: View detailed user data"""
    users = storage.load_users() or []
    all_tasks = storage.load_tasks() or []
    
    data_win = tk.Toplevel(root)
    data_win.title("All User Data - VULNERABLE")
    data_win.geometry("800x600")
    
    text_area = scrolledtext.ScrolledText(data_win, width=90, height=30)
    text_area.pack(fill='both', expand=True, padx=20, pady=20)
    
    content = "VULNERABLE DATA ACCESS: All User Information\n"
    content += "=" * 60 + "\n\n"
    
    for user in users:
        user_tasks = [t for t in all_tasks if t['owner_id'] == user['id']]
        completed = sum(1 for t in user_tasks if t.get('done'))
        
        content += f"USER: {user['username']}\n"
        content += f"  ID: {user['id']} | Admin: {user.get('is_admin', False)}\n"
        content += f"  Created: {user.get('created_at', 'Unknown')}\n"
        content += f"  Tasks: {len(user_tasks)} (Completed: {completed})\n"
        
        if user_tasks:
            content += "  Recent Tasks:\n"
            for task in user_tasks[:5]:  # Show recent 5 tasks
                status = "✓" if task.get('done') else "○"
                content += f"    {status} {task['title']}\n"
        content += "\n"
    
    text_area.insert('1.0', content)
    text_area.config(state='disabled')
    
    center_window(data_win)

def vulnerable_maintenance():
    """Vulnerable maintenance - No admin check"""
    # VULNERABLE: Any user can perform maintenance
    choice = messagebox.askyesno("Maintenance", 
                                "VULNERABLE: Maintenance functions available to all users\n\n"
                                "Yes: Create backup\nNo: Generate sample data")
    
    if choice:
        backup_path = maintenance.backup_data()
        messagebox.showinfo("Backup", f"Backup created: {backup_path}")
    else:
        users = simpledialog.askinteger("Sample Data", "Users to create:", initialvalue=5)
        if users:
            tasks_per = simpledialog.askinteger("Sample Data", "Tasks per user:", initialvalue=3)
            if tasks_per:
                result = maintenance.generate_sample_data(users, tasks_per)
                messagebox.showinfo("Sample Data", 
                                  f"Created {result['created_users']} users and {result['created_tasks']} tasks")

def create_admin_user():
    """Vulnerable: Create admin user without privileges"""
    # VULNERABLE: Any user can create admin accounts
    username = simpledialog.askstring("Create Admin", "Username for new admin:")
    if username:
        password = simpledialog.askstring("Create Admin", "Password:", show="*")
        if password:
            user = auth.register_user(username, password, is_admin=True)
            if user:
                messagebox.showinfo("Success", f"Admin user '{username}' created")
            else:
                messagebox.showerror("Error", "User creation failed")

def quit_app():
    """Quit application"""
    if messagebox.askokcancel("Quit", "Quit vulnerable TodoApp?"):
        root.destroy()

def refresh_main_menu():
    """Refresh main menu"""
    global main_frame, user_lbl
    
    for widget in main_frame.winfo_children():
        if widget != user_lbl:
            widget.destroy()
    
    set_user_label(user_lbl, CURRENT_USER)
    
    menu_frame = create_modern_frame(main_frame, 30)
    menu_frame.pack(expand=True)
    
    # Security warning
    warning_frame = create_modern_frame(menu_frame, 15)
    warning_frame.pack(fill='x', pady=(0, 20))
    
    ttk.Label(warning_frame, text="⚠️  VULNERABLE VERSION", 
             foreground='red', font=('Arial', 14, 'bold')).pack()
    ttk.Label(warning_frame, text="CWE-306: Missing Authentication for Critical Function", 
             foreground='red', font=('Arial', 10)).pack()
    
    # Menu buttons
    if not CURRENT_USER:
        create_modern_button(menu_frame, "Login", 
                           lambda: login(user_lbl), 
                           'Primary.TButton', 25).pack(fill='x', pady=8)
    else:
        create_modern_button(menu_frame, "Logout", 
                           logout, 
                           'Secondary.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(menu_frame, "Register", 
                       register, 
                       'Success.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(menu_frame, "Task Manager", 
                       open_user_panel, 
                       'Primary.TButton', 25).pack(fill='x', pady=8)
    
    # VULNERABLE: Admin tools always available
    create_modern_button(menu_frame, "Admin Tools (VULNERABLE)", 
                       admin_tools, 
                       'Danger.TButton', 25).pack(fill='x', pady=8)
    
    create_modern_button(menu_frame, "Quit", 
                       quit_app, 
                       'Secondary.TButton', 25).pack(fill='x', pady=8)
    
    # Educational info
    info_frame = create_modern_frame(menu_frame, 15)
    info_frame.pack(fill='x', pady=(20, 0))
    
    ttk.Label(info_frame, text="Security Vulnerabilities Present:", 
             font=('Arial', 10, 'bold')).pack()
    ttk.Label(info_frame, text="• No admin authentication • View all user data • Modify any tasks", 
             font=('Arial', 9)).pack()

def initialize_vulnerable_app():
    """Initialize vulnerable application"""
    global root, main_container, main_frame, user_lbl
    
    root = tk.Tk()
    root.title("TodoApp - Vulnerable GUI - CWE-306 Demo")
    root.geometry("700x600")
    root.minsize(600, 500)
    
    setup_styles()
    
    main_container = create_modern_frame(root, 0)
    main_container.pack(fill='both', expand=True, padx=40, pady=30)
    
    # Header with vulnerability emphasis
    header_frame = create_header(main_container, 
                               "TodoApp - Vulnerable Version", 
                               "CWE-306: Missing Authentication for Critical Function")
    
    # User status
    user_section = create_modern_frame(main_container, 15)
    user_section.pack(fill='x', pady=(0, 20))
    
    ttk.Label(user_section, text="Session Status", 
             style='Header.TLabel').pack(anchor='w', pady=(0, 8))
    
    user_lbl = ttk.Label(user_section, text="User: Not logged in", 
                        font=('Arial', 11))
    user_lbl.pack(anchor='w')
    
    main_frame = create_modern_frame(main_container, 0)
    main_frame.pack(fill='both', expand=True)
    
    refresh_main_menu()
    center_window(root)
    
    return root

if __name__ == "__main__":
    app = initialize_vulnerable_app()
    app.mainloop()