'''
Professional admin tools and maintenance panels
'''

# Track open windows
_open_windows = {}

def admin_tools(root, CURRENT_USER, auth_module, fixed_module, storage_module, maintenance_module, refresh_main_callback):
    """Professional admin tools interface"""
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    from .session import AuthenticatedAdminSession
    from .gui_styles import create_modern_frame, create_modern_button, COLORS
    from .gui_components import create_header, center_window
    
    # Prevent multiple admin panels
    if 'admin_tools' in _open_windows and _open_windows['admin_tools'].winfo_exists():
        _open_windows['admin_tools'].lift()
        return _open_windows['admin_tools']
    
    admin_session = None
    
    # Authenticate admin if not already authenticated
    if not CURRENT_USER or not CURRENT_USER.get("is_admin"):
        username = simpledialog.askstring("Admin Authentication", 
                                        "Administrator Username:",
                                        parent=root)
        if not username:
            return None
            
        password = simpledialog.askstring("Admin Authentication", 
                                        "Administrator Password:",
                                        parent=root,
                                        show="*")
        if not password:
            return None
        
        admin_session = auth_module.login_user(username, password, require_admin_session=True)
        
        if not admin_session or not isinstance(admin_session, AuthenticatedAdminSession) or not admin_session.is_valid():
            messagebox.showerror("Authentication Failed", 
                               "Invalid administrator credentials or insufficient privileges.")
            return None
    else:
        # Already logged in as admin
        admin_session = AuthenticatedAdminSession(CURRENT_USER)
    
    # Create admin window
    admin_win = tk.Toplevel(root)
    _open_windows['admin_tools'] = admin_win
    admin_win.title("Administrator Tools - TodoApp")
    admin_win.geometry("600x500")
    admin_win.minsize(500, 400)
    
    # Header
    header_frame = create_header(admin_win, "Administrator Tools", 
                               "System management and maintenance")
    
    # Main content
    content_frame = create_modern_frame(admin_win, 30)
    content_frame.pack(fill='both', expand=True, padx=40, pady=20)
    
    # Admin options
    create_modern_button(content_frame, "Task Management", 
                        lambda: admin_task_management(admin_win, admin_session, storage_module, fixed_module, refresh_main_callback), 
                        'Primary.TButton', 25).pack(fill='x', pady=12)
    
    create_modern_button(content_frame, "System Maintenance", 
                        lambda: system_maintenance(admin_win, admin_session, maintenance_module), 
                        'Warning.TButton', 25).pack(fill='x', pady=12)
    
    create_modern_button(content_frame, "User Statistics", 
                        lambda: show_user_stats(admin_win, storage_module, maintenance_module), 
                        'Secondary.TButton', 25).pack(fill='x', pady=12)
    
    create_modern_button(content_frame, "Close Admin Tools", 
                        admin_win.destroy, 
                        'Danger.TButton', 25).pack(fill='x', pady=12)
    
    def cleanup():
        """Clean up window tracking"""
        _open_windows.pop('admin_tools', None)
        admin_win.destroy()
    
    admin_win.protocol("WM_DELETE_WINDOW", cleanup)
    center_window(admin_win)
    
    return admin_win

def admin_task_management(parent, admin_session, storage_module, fixed_module, refresh_main_callback):
    """Professional admin task management"""
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    from .gui_styles import create_modern_frame, create_modern_button, create_scrolled_text, COLORS
    from .gui_components import create_header, center_window, create_section_label
    
    # Prevent multiple task management windows
    if 'admin_tasks' in _open_windows and _open_windows['admin_tasks'].winfo_exists():
        _open_windows['admin_tasks'].lift()
        return
    
    tasks_win = tk.Toplevel(parent)
    _open_windows['admin_tasks'] = tasks_win
    tasks_win.title("Admin Task Management - TodoApp")
    tasks_win.geometry("1000x700")
    tasks_win.minsize(900, 600)
    
    # Header
    header_frame = create_header(tasks_win, "Administrative Task Management", 
                               "Manage all system tasks")
    
    # Action toolbar
    toolbar_frame = create_modern_frame(tasks_win, 15)
    toolbar_frame.pack(fill='x', padx=40, pady=(0, 20))
    
    create_modern_button(toolbar_frame, "Delete All Tasks", 
                        lambda: delete_all_tasks(admin_session, storage_module, fixed_module, refresh_main_callback, refresh_view), 
                        'Danger.TButton', 18).grid(row=0, column=0, padx=6, pady=6)
    
    create_modern_button(toolbar_frame, "Refresh View", 
                        refresh_view, 
                        'Secondary.TButton', 18).grid(row=0, column=1, padx=6, pady=6)
    
    create_modern_button(toolbar_frame, "Export Tasks", 
                        lambda: export_tasks(storage_module), 
                        'Success.TButton', 18).grid(row=0, column=2, padx=6, pady=6)
    
    create_modern_button(toolbar_frame, "Close", 
                        tasks_win.destroy, 
                        'Secondary.TButton', 18).grid(row=0, column=3, padx=6, pady=6)
    
    # Tasks display
    content_frame = create_modern_frame(tasks_win, 20)
    content_frame.pack(fill='both', expand=True, padx=40, pady=10)
    
    create_section_label(content_frame, "All System Tasks").pack(anchor='w', pady=(0, 12))
    
    task_display = create_scrolled_text(content_frame, width=95, height=25)
    task_display.pack(fill='both', expand=True)
    task_display.config(state=tk.DISABLED)
    
    def delete_all_tasks(session, storage, fixed, refresh_main, refresh_callback):
        """Securely delete all tasks with admin authentication"""
        if not messagebox.askyesno("Confirm Delete All", 
                                  "WARNING: This will permanently delete ALL tasks for ALL users!\n\n"
                                  "This action cannot be undone.\n\n"
                                  "Are you absolutely sure you want to continue?",
                                  icon='warning'):
            return
            
        try:
            if hasattr(fixed, "delete_all_tasks_fixed"):
                success = fixed.delete_all_tasks_fixed(session)
                if success:
                    messagebox.showinfo("Success", "All tasks have been deleted successfully.")
                else:
                    messagebox.showerror("Error", "Delete operation failed: Not authorized.")
            else:
                storage.save_tasks([])
                storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={getattr(session, 'id', '?')}")
                messagebox.showinfo("Success", "All tasks have been deleted.")
            
            refresh_main()
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Delete operation failed: {str(e)}")
    
    def export_tasks(storage):
        """Export tasks to a readable format"""
        tasks = storage.load_tasks() or []
        if not tasks:
            messagebox.showinfo("Export", "No tasks to export.")
            return
        
        export_text = f"TodoApp Task Export - {len(tasks)} tasks\n"
        export_text += "=" * 50 + "\n\n"
        
        for task in tasks:
            export_text += f"Task ID: {task.get('id')}\n"
            export_text += f"Owner ID: {task.get('owner_id')}\n"
            export_text += f"Title: {task.get('title')}\n"
            export_text += f"Status: {'COMPLETED' if task.get('done') else 'PENDING'}\n"
            export_text += f"Description: {task.get('description', '')}\n"
            export_text += f"Created: {task.get('created_at')}\n"
            export_text += "-" * 30 + "\n"
        
        # Show in a dialog (could be enhanced to save to file)
        show_export_dialog(export_text)
    
    def show_export_dialog(content):
        """Show export content in a dialog"""
        export_win = tk.Toplevel(tasks_win)
        export_win.title("Task Export - TodoApp")
        export_win.geometry("700x500")
        
        frame = create_modern_frame(export_win, 20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Task Export", style='Title.TLabel').pack(pady=(0, 15))
        
        export_text = scrolledtext.ScrolledText(frame, width=80, height=25, font=('Consolas', 9))
        export_text.pack(fill='both', expand=True)
        export_text.insert('1.0', content)
        export_text.config(state=tk.DISABLED)
        
        create_modern_button(frame, "Close", export_win.destroy, 'Secondary.TButton').pack(pady=(15, 0))
        
        center_window(export_win)
    
    def refresh_view():
        """Refresh the task view with all system tasks"""
        tasks_all = storage_module.load_tasks() or []
        task_display.config(state=tk.NORMAL)
        task_display.delete("1.0", tk.END)
        
        if not tasks_all:
            task_display.insert(tk.END, "No tasks found in the system.\n\n", "center")
            task_display.insert(tk.END, "Users can create tasks through the main application.", "hint")
        else:
            # Statistics header
            completed = sum(1 for t in tasks_all if t.get('done'))
            pending = len(tasks_all) - completed
            
            task_display.insert(tk.END, f"System Task Overview\n", "header")
            task_display.insert(tk.END, f"Total Tasks: {len(tasks_all)} | ", "stats")
            task_display.insert(tk.END, f"Completed: {completed} | ", "completed_stats")
            task_display.insert(tk.END, f"Pending: {pending}\n\n", "pending_stats")
            
            # Task list
            for task in tasks_all:
                status = "COMPLETED" if task.get('done') else "PENDING"
                status_tag = "completed" if task.get('done') else "pending"
                
                task_display.insert(tk.END, f"[{status}] ", status_tag)
                task_display.insert(tk.END, f"ID: {task.get('id')} | ", "normal")
                task_display.insert(tk.END, f"Owner: {task.get('owner_id')} | ", "normal")
                task_display.insert(tk.END, f"Title: {task.get('title')}\n", "title")
                
                if task.get('description'):
                    task_display.insert(tk.END, f"      Description: {task.get('description')}\n", "description")
                
                task_display.insert(tk.END, f"      Created: {task.get('created_at')}\n\n", "date")
        
        # Configure text tags
        task_display.tag_configure("center", justify='center', foreground=COLORS['text_secondary'])
        task_display.tag_configure("hint", justify='center', foreground=COLORS['text_secondary'], font=('Arial', 9))
        task_display.tag_configure("header", foreground=COLORS['primary'], font=('Arial', 12, 'bold'))
        task_display.tag_configure("stats", foreground=COLORS['text_primary'], font=('Arial', 10, 'bold'))
        task_display.tag_configure("completed_stats", foreground=COLORS['success'], font=('Arial', 10, 'bold'))
        task_display.tag_configure("pending_stats", foreground=COLORS['warning'], font=('Arial', 10, 'bold'))
        task_display.tag_configure("title", foreground=COLORS['text_primary'], font=('Arial', 10, 'bold'))
        task_display.tag_configure("normal", foreground=COLORS['text_primary'], font=('Arial', 10))
        task_display.tag_configure("description", foreground=COLORS['text_secondary'], font=('Arial', 9))
        task_display.tag_configure("date", foreground=COLORS['text_secondary'], font=('Arial', 9))
        task_display.tag_configure("completed", foreground=COLORS['success'], font=('Arial', 10, 'bold'))
        task_display.tag_configure("pending", foreground=COLORS['warning'], font=('Arial', 10, 'bold'))
        
        task_display.config(state=tk.DISABLED)
    
    def cleanup():
        """Clean up window tracking"""
        _open_windows.pop('admin_tasks', None)
        tasks_win.destroy()
    
    tasks_win.protocol("WM_DELETE_WINDOW", cleanup)
    refresh_view()
    center_window(tasks_win)
    
    return tasks_win

def system_maintenance(parent, admin_session, maintenance_module):
    """System maintenance functions"""
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    
    if not admin_session or not admin_session.is_admin:
        messagebox.showerror("Access Denied", "Administrator privileges required for system maintenance.")
        return
    
    # Show maintenance options
    choice = messagebox.askyesno("System Maintenance", 
                                "System Maintenance Options:\n\n"
                                "Yes: Create system backup\n"
                                "No: Generate sample data\n\n"
                                "Choose operation:")
    
    if choice:
        # Create backup
        backup_path = maintenance_module.backup_data()
        messagebox.showinfo("Backup Complete", f"System backup created successfully:\n{backup_path}")
    else:
        # Generate sample data
        users = simpledialog.askinteger("Sample Data", 
                                      "Number of sample users to create:",
                                      parent=parent,
                                      initialvalue=5,
                                      minvalue=1,
                                      maxvalue=50)
        
        if users:
            tasks_per_user = simpledialog.askinteger("Sample Data", 
                                                   "Tasks per user:",
                                                   parent=parent,
                                                   initialvalue=3,
                                                   minvalue=1,
                                                   maxvalue=20)
            
            if tasks_per_user:
                result = maintenance_module.generate_sample_data(users, tasks_per_user)
                messagebox.showinfo("Sample Data Generated", 
                                  f"Successfully created:\n"
                                  f"- {result['created_users']} users\n"
                                  f"- {result['created_tasks']} tasks")

def show_user_stats(parent, storage_module, maintenance_module):
    """Display user and system statistics"""
    import tkinter as tk
    from tkinter import ttk, scrolledtext
    from .gui_styles import create_modern_frame, create_modern_button
    from .gui_components import center_window
    
    stats_win = tk.Toplevel(parent)
    stats_win.title("System Statistics - TodoApp")
    stats_win.geometry("500x400")
    stats_win.resizable(False, False)
    
    frame = create_modern_frame(stats_win, 25)
    frame.pack(fill='both', expand=True)
    
    ttk.Label(frame, text="System Statistics", style='Title.TLabel').pack(pady=(0, 20))
    
    # Get statistics
    stats = maintenance_module.stats()
    users = storage_module.load_users() or []
    tasks = storage_module.load_tasks() or []
    
    # Calculate additional stats
    admin_users = sum(1 for u in users if u.get('is_admin'))
    regular_users = len(users) - admin_users
    completed_tasks = sum(1 for t in tasks if t.get('done'))
    
    # Display statistics
    stats_text = scrolledtext.ScrolledText(frame, width=55, height=15, font=('Arial', 10))
    stats_text.pack(fill='both', expand=True, pady=(0, 20))
    
    stats_content = f"""SYSTEM STATISTICS
{'-' * 50}

USER STATISTICS:
• Total Users: {stats.get('users', 0)}
• Administrators: {admin_users}
• Regular Users: {regular_users}

TASK STATISTICS:
• Total Tasks: {stats.get('tasks', 0)}
• Completed Tasks: {completed_tasks}
• Pending Tasks: {stats.get('tasks', 0) - completed_tasks}

SYSTEM INFORMATION:
• Data Directory: {getattr(storage_module, 'DATA_DIR', 'Not specified')}
• Users File: {getattr(storage_module, 'USERS_FILE', 'Not specified')}
• Tasks File: {getattr(storage_module, 'TASKS_FILE', 'Not specified')}

Last Updated: {getattr(storage_module, 'get_current_time', lambda: 'Unknown')()}
"""
    
    stats_text.insert('1.0', stats_content)
    stats_text.config(state=tk.DISABLED)
    
    create_modern_button(frame, "Close", stats_win.destroy, 'Secondary.TButton').pack()
    
    center_window(stats_win)