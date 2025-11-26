'''
Admin tools and maintenance panels
'''

def admin_tools(root, CURRENT_USER, auth, fixed, storage, maintenance, refresh_main_menu_callback):
    """Modern admin tools interface"""
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog
    from .session import AuthenticatedAdminSession
    from .gui_styles import create_modern_frame, create_modern_button, COLORS
    from .gui_components import create_header
    
    admin_session = None
    
    # Authenticate admin
    if not CURRENT_USER or not CURRENT_USER.get("is_admin"):
        # Show authentication dialog
        username = simpledialog.askstring("Admin Auth", "Admin username:")
        if not username:
            return None
            
        password = simpledialog.askstring("Admin Auth", "Admin password:", show="*")
        admin_session = auth.login_user(username, password, require_admin_session=True)
        
        if not admin_session or not isinstance(admin_session, AuthenticatedAdminSession) or not admin_session.is_valid():
            messagebox.showerror("Admin", "❌ Authentication failed. Cannot open Admin Tools.")
            return None
    else:
        # Already logged in as admin
        admin_session = AuthenticatedAdminSession(CURRENT_USER)
    
    # Create admin window
    admin_win = tk.Toplevel(root)
    admin_win.title("🛠️ Admin Tools")
    admin_win.geometry("600x400")
    
    # Header
    header_frame = create_header(admin_win, "🛠️ Administrator Tools", 
                               "System management and maintenance")
    
    # Main content
    content_frame = create_modern_frame(admin_win, 20)
    content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Admin options
    create_modern_button(content_frame, "📊 Admin Menu", 
                        lambda: admin_menu(admin_win, admin_session, storage, fixed, refresh_main_menu_callback), 
                        'Primary.TButton', 25).pack(fill='x', pady=10)
    create_modern_button(content_frame, "🔧 Maintenance", 
                        lambda: open_maintenance_window(admin_win, admin_session, maintenance), 
                        'Secondary.TButton', 25).pack(fill='x', pady=10)
    create_modern_button(content_frame, "❌ Close", 
                        admin_win.destroy, 
                        'Danger.TButton', 25).pack(fill='x', pady=10)
    
    return admin_win

def admin_menu(parent, admin_session, storage, fixed, refresh_user_tasks_callback):
    """Admin menu with task management"""
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    from .gui_styles import create_modern_frame, create_modern_button, create_scrolled_text, COLORS
    from .gui_components import create_header
    
    sub = tk.Toplevel(parent)
    sub.title("📊 Admin Menu - Task Management")
    sub.geometry("900x600")
    
    # Header
    header_frame = create_header(sub, "📊 Admin Task Management")
    
    # Action buttons
    button_frame = create_modern_frame(sub, 10)
    button_frame.pack(fill='x', padx=20, pady=(0, 10))
    
    create_modern_button(button_frame, "🗑️ Delete ALL Tasks", 
                        lambda: do_delete_all_fixed(admin_session, storage, fixed, refresh_user_tasks_callback, refresh_view), 
                        'Danger.TButton', 20).grid(row=0, column=0, padx=5, pady=5)
    create_modern_button(button_frame, "🔄 Refresh View", 
                        refresh_view, 
                        'Secondary.TButton', 20).grid(row=0, column=1, padx=5, pady=5)
    create_modern_button(button_frame, "❌ Close", 
                        sub.destroy, 
                        'Secondary.TButton', 20).grid(row=0, column=2, padx=5, pady=5)
    
    # Tasks display
    tasks_frame = create_modern_frame(sub, 10)
    tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    ttk.Label(tasks_frame, text="All System Tasks:", font=('Arial', 12, 'bold')).pack(anchor='w')
    
    task_display = create_scrolled_text(tasks_frame, font=('Consolas', 9))
    task_display.pack(fill='both', expand=True, pady=(10, 0))
    task_display.config(state=tk.DISABLED)
    
    def do_delete_all_fixed(session, storage, fixed, refresh_user_callback, refresh_view_callback):
        """Securely delete all tasks with admin authentication"""
        if not messagebox.askyesno("Confirm Delete", 
                                  "🚨 WARNING: This will delete ALL tasks for ALL users!\n\nThis action cannot be undone.\n\nAre you absolutely sure?"):
            return
            
        try:
            if hasattr(fixed, "delete_all_tasks_fixed"):
                ok = fixed.delete_all_tasks_fixed(session)
                if ok:
                    messagebox.showinfo("Success", "✅ All tasks deleted successfully!")
                else:
                    messagebox.showerror("Error", "❌ Delete failed (not authorized)")
            else:
                storage.save_tasks([])
                storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={getattr(session, 'id', '?')}")
                messagebox.showinfo("Success", "✅ All tasks deleted!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Delete failed: {e}")
            
        refresh_user_callback()
        refresh_view_callback()
    
    def refresh_view():
        """Refresh the task view"""
        tasks_all = storage.load_tasks() or []
        task_display.config(state=tk.NORMAL)
        task_display.delete("1.0", tk.END)
        
        if not tasks_all:
            task_display.insert(tk.END, "📝 No tasks in the system\n", "center")
        else:
            task_display.insert(tk.END, f"Total Tasks: {len(tasks_all)}\n\n", "header")
            for t in tasks_all:
                status_icon = "✅" if t.get("done") else "⏳"
                task_display.insert(tk.END, f"{status_icon} ", "icon")
                task_display.insert(tk.END, f"ID: {t.get('id')} | Owner: {t.get('owner_id')} | ", "normal")
                task_display.insert(tk.END, f"Title: {t.get('title')}\n", "title")
                if t.get('description'):
                    task_display.insert(tk.END, f"     Description: {t.get('description','')}\n", "desc")
                task_display.insert(tk.END, f"     Created: {t.get('created_at','')}\n\n", "date")
        
        # Configure text styles
        task_display.tag_configure("center", justify='center', foreground=COLORS['secondary'])
        task_display.tag_configure("header", font=('Arial', 10, 'bold'))
        task_display.tag_configure("title", font=('Arial', 10, 'bold'))
        task_display.tag_configure("normal", font=('Consolas', 9))
        task_display.tag_configure("desc", font=('Consolas', 9), foreground=COLORS['secondary'])
        task_display.tag_configure("date", font=('Consolas', 8), foreground=COLORS['secondary'])
        task_display.tag_configure("icon", font=('Arial', 9))
        
        task_display.config(state=tk.DISABLED)
    
    refresh_view()
    return sub

def open_maintenance_window(parent, admin, maintenance):
    """Modern maintenance window"""
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog, scrolledtext
    from .gui_styles import create_modern_frame, create_modern_button, COLORS
    from .gui_components import create_header
    
    win = tk.Toplevel(parent)
    win.title("🔧 System Maintenance")
    win.geometry("700x500")
    
    # Header
    header_frame = create_header(win, "🔧 System Maintenance", 
                               "Database management and system utilities")
    
    # Content
    content_frame = create_modern_frame(win, 20)
    content_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    # Stats display
    stats_frame = create_modern_frame(content_frame, 15)
    stats_frame.pack(fill='x', pady=(0, 20))
    
    ttk.Label(stats_frame, text="System Statistics", font=('Arial', 14, 'bold')).pack(anchor='w', pady=(0, 10))
    
    out = scrolledtext.ScrolledText(stats_frame, width=80, height=8,
                                   font=('Consolas', 9),
                                   bg=COLORS['surface'],
                                   relief='flat')
    out.pack(fill='both', expand=True)
    out.config(state=tk.DISABLED)
    
    # Maintenance buttons
    button_frame = ttk.Frame(content_frame)
    button_frame.pack(fill='x')
    
    create_modern_button(button_frame, "📈 Show Stats", 
                        lambda: show_stats(out, maintenance), 
                        'Primary.TButton', 18).grid(row=0, column=0, padx=5, pady=5)
    create_modern_button(button_frame, "💾 Backup Data", 
                        lambda: do_backup(admin, maintenance), 
                        'Success.TButton', 18).grid(row=0, column=1, padx=5, pady=5)
    create_modern_button(button_frame, "🔄 Restore Backup", 
                        lambda: do_restore(admin, maintenance), 
                        'Warning.TButton', 18).grid(row=1, column=0, padx=5, pady=5)
    create_modern_button(button_frame, "🎲 Generate Sample Data", 
                        lambda: do_generate(maintenance), 
                        'Secondary.TButton', 18).grid(row=1, column=1, padx=5, pady=5)
    create_modern_button(button_frame, "❌ Close", 
                        win.destroy, 
                        'Danger.TButton', 18).grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')
    
    def show_stats(out_widget, maintenance_module):
        """Display system statistics"""
        s = maintenance_module.stats()
        out_widget.config(state=tk.NORMAL)
        out_widget.delete("1.0", tk.END)
        out_widget.insert(tk.END, "📊 SYSTEM STATISTICS\n")
        out_widget.insert(tk.END, "=" * 50 + "\n\n")
        out_widget.insert(tk.END, f"👥 Total Users: {s.get('users', 0)}\n")
        out_widget.insert(tk.END, f"📝 Total Tasks: {s.get('tasks', 0)}\n")
        out_widget.config(state=tk.DISABLED)
    
    def do_backup(admin_user, maintenance_module):
        """Create backup with admin authentication"""
        if not admin_user or not admin_user.get("is_admin"):
            messagebox.showerror("Error", "🔒 Admin privileges required for backup")
            return
        p = maintenance_module.backup_data()
        messagebox.showinfo("Success", f"✅ Backup created:\n{p}")
    
    def do_restore(admin_user, maintenance_module):
        """Restore backup with admin authentication"""
        if not admin_user or not admin_user.get("is_admin"):
            messagebox.showerror("Error", "🔒 Admin privileges required for restore")
            return
        name = simpledialog.askstring("Restore Backup", "Enter backup name or directory:")
        if not name:
            return
        ok = maintenance_module.restore_backup(name)
        messagebox.showinfo("Result", "✅ Restore succeeded!" if ok else "❌ Restore failed")
    
    def do_generate(maintenance_module):
        """Generate sample data"""
        u = simpledialog.askstring("Generate Data", "Number of users to create (default 10):")
        t = simpledialog.askstring("Generate Data", "Tasks per user (default 10):")
        try:
            nu = int(u) if u else 10
            nt = int(t) if t else 10
        except ValueError:
            messagebox.showerror("Error", "❌ Please enter valid numbers")
            return
        res = maintenance_module.generate_sample_data(nu, nt)
        messagebox.showinfo("Success", f"✅ Generated {res['created_users']} users and {res['created_tasks']} tasks")
    
    show_stats(out, maintenance)
    return win