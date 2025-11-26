'''
User task management panel
'''

def refresh_user_tasks_display(user_tasks_text, CURRENT_USER, tasks, COLORS):
    """Refresh the task display with modern formatting"""
    import tkinter as tk
    from tkinter import ttk
    
    if not user_tasks_text or not hasattr(user_tasks_text, 'winfo_exists') or not user_tasks_text.winfo_exists():
        return
        
    user_tasks_text.config(state=tk.NORMAL)
    user_tasks_text.delete("1.0", tk.END)
    
    if not CURRENT_USER:
        user_tasks_text.insert(tk.END, "🔒 Please log in to view your tasks\n", "center")
    else:
        my_tasks = tasks.list_tasks_for_user(CURRENT_USER["id"])
        if not my_tasks:
            user_tasks_text.insert(tk.END, "📝 No tasks found. Create your first task!\n", "center")
        else:
            for t in my_tasks:
                status_icon = "✅" if t.get("done") else "⏳"
                status_text = "COMPLETED" if t.get("done") else "PENDING"
                
                user_tasks_text.insert(tk.END, f"{status_icon} ", "icon")
                user_tasks_text.insert(tk.END, f"Task #{t.get('id')}: {t.get('title')}\n", "title")
                user_tasks_text.insert(tk.END, f"   Status: {status_text}\n", "status")
                if t.get('description'):
                    user_tasks_text.insert(tk.END, f"   Description: {t.get('description','')}\n", "normal")
                user_tasks_text.insert(tk.END, f"   Created: {t.get('created_at','')}\n\n", "date")
    
    # Configure text tags for styling
    user_tasks_text.tag_configure("center", justify='center', foreground=COLORS['secondary'])
    user_tasks_text.tag_configure("title", font=('Arial', 11, 'bold'))
    user_tasks_text.tag_configure("status", foreground=COLORS['secondary'])
    user_tasks_text.tag_configure("date", foreground=COLORS['secondary'], font=('Arial', 9))
    user_tasks_text.tag_configure("icon", font=('Arial', 11))
    user_tasks_text.tag_configure("normal", font=('Arial', 10))
    
    user_tasks_text.config(state=tk.DISABLED)

def open_user_panel(root, CURRENT_USER, tasks, refresh_user_tasks_callback):
    """Modern user panel with task management"""
    import tkinter as tk
    from tkinter import ttk, simpledialog, messagebox
    from .gui_styles import create_modern_frame, create_modern_button, create_scrolled_text, COLORS
    from .gui_components import create_header
    
    user_win = tk.Toplevel(root)
    user_win.title("🎯 Task Manager - User Panel")
    user_win.geometry("800x600")
    
    # Header
    header_frame = create_header(user_win, "🎯 Task Manager", 
                               f"Welcome, {CURRENT_USER['username']}!" if CURRENT_USER else None)
    
    # Action buttons
    button_frame = create_modern_frame(user_win, 10)
    button_frame.pack(fill='x', padx=20, pady=(0, 10))
    
    create_modern_button(button_frame, "➕ Create Task", 
                        lambda: create_task_dialog(root, CURRENT_USER, tasks, refresh_user_tasks_callback), 
                        'Success.TButton', 15).grid(row=0, column=0, padx=5, pady=5)
    create_modern_button(button_frame, "✅ Complete Task", 
                        lambda: complete_task_dialog(root, CURRENT_USER, tasks, refresh_user_tasks_callback), 
                        'Primary.TButton', 15).grid(row=0, column=1, padx=5, pady=5)
    create_modern_button(button_frame, "✏️ Edit Task", 
                        lambda: edit_task_dialog(root, CURRENT_USER, tasks, refresh_user_tasks_callback), 
                        'Secondary.TButton', 15).grid(row=0, column=2, padx=5, pady=5)
    create_modern_button(button_frame, "🗑️ Delete Task", 
                        lambda: delete_task_dialog(root, CURRENT_USER, tasks, refresh_user_tasks_callback), 
                        'Danger.TButton', 15).grid(row=0, column=3, padx=5, pady=5)
    create_modern_button(button_frame, "🔄 Refresh", 
                        refresh_user_tasks_callback, 
                        'Secondary.TButton', 15).grid(row=0, column=4, padx=5, pady=5)
    
    # Tasks display
    tasks_frame = create_modern_frame(user_win, 10)
    tasks_frame.pack(fill='both', expand=True, padx=20, pady=10)
    
    ttk.Label(tasks_frame, text="Your Tasks:", font=('Arial', 12, 'bold')).pack(anchor='w')
    
    user_tasks_text = create_scrolled_text(tasks_frame)
    user_tasks_text.pack(fill='both', expand=True, pady=(10, 0))
    
    return user_win, user_tasks_text

def create_task_dialog(root, CURRENT_USER, tasks, refresh_callback):
    """Create task dialog"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button
    
    if not CURRENT_USER:
        messagebox.showwarning("Warning", "🔒 Please log in first")
        return
        
    create_win = tk.Toplevel(root)
    create_win.title("Create New Task")
    create_win.geometry("400x300")
    create_win.resizable(False, False)
    
    frame = create_modern_frame(create_win, 20)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    ttk.Label(frame, text="➕ Create New Task", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
    
    # Title
    ttk.Label(frame, text="Task Title:*", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 0))
    title_var = tk.StringVar()
    title_entry = ttk.Entry(frame, textvariable=title_var, width=30, font=('Arial', 11))
    title_entry.pack(fill='x', pady=(5, 15))
    title_entry.focus()
    
    # Description
    ttk.Label(frame, text="Description:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 0))
    desc_text = tk.Text(frame, width=30, height=6, font=('Arial', 10), wrap='word')
    desc_text.pack(fill='both', pady=(5, 20))
    
    def perform_create():
        title = title_var.get().strip()
        desc = desc_text.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showerror("Error", "❌ Task title is required")
            return
            
        t = tasks.add_task(CURRENT_USER["id"], title, desc)
        messagebox.showinfo("Success", f"✅ Task created successfully!\nTask ID: {t['id']}")
        create_win.destroy()
        refresh_callback()
    
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill='x')
    
    create_modern_button(button_frame, "Create Task", perform_create, 'Success.TButton').pack(side='right', padx=(5, 0))
    create_modern_button(button_frame, "Cancel", create_win.destroy, 'Secondary.TButton').pack(side='right')

def complete_task_dialog(root, CURRENT_USER, tasks, refresh_callback):
    """Complete task dialog"""
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    if not CURRENT_USER:
        messagebox.showwarning("Warning", "🔒 Please log in first")
        return
        
    tid = simpledialog.askinteger("Complete Task", "Enter Task ID to mark complete:")
    if tid is None:
        return
        
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Error", "❌ Task not found")
        return
        
    if t["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Error", "🚫 You are not the owner of this task")
        return
        
    tasks.update_task(tid, done=True)
    messagebox.showinfo("Success", "✅ Task marked as complete!")
    refresh_callback()

def edit_task_dialog(root, CURRENT_USER, tasks, refresh_callback):
    """Edit task dialog"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    if not CURRENT_USER:
        messagebox.showwarning("Warning", "🔒 Please log in first")
        return
        
    tid = simpledialog.askinteger("Edit Task", "Enter Task ID to edit:")
    if tid is None:
        return
        
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Error", "❌ Task not found")
        return
        
    if t["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Error", "🚫 You are not the owner of this task")
        return
        
    # Custom edit dialog
    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Task")
    edit_win.geometry("400x350")
    edit_win.resizable(False, False)
    
    frame = create_modern_frame(edit_win, 20)
    frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    ttk.Label(frame, text="✏️ Edit Task", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
    
    # Title
    ttk.Label(frame, text="Task Title:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 0))
    title_var = tk.StringVar(value=t['title'])
    title_entry = ttk.Entry(frame, textvariable=title_var, width=30, font=('Arial', 11))
    title_entry.pack(fill='x', pady=(5, 15))
    
    # Description
    ttk.Label(frame, text="Description:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(5, 0))
    desc_text = tk.Text(frame, width=30, height=6, font=('Arial', 10), wrap='word')
    desc_text.pack(fill='both', pady=(5, 15))
    desc_text.insert("1.0", t.get('description', ''))
    
    # Completion status
    done_var = tk.BooleanVar(value=t.get('done', False))
    ttk.Checkbutton(frame, text="Mark as completed", 
                   variable=done_var).pack(anchor='w', pady=(5, 20))
    
    def perform_edit():
        new_title = title_var.get().strip()
        new_desc = desc_text.get("1.0", tk.END).strip()
        
        if not new_title:
            messagebox.showerror("Error", "❌ Task title is required")
            return
            
        tasks.update_task(tid, title=new_title, description=new_desc, done=done_var.get())
        messagebox.showinfo("Success", "✅ Task updated successfully!")
        edit_win.destroy()
        refresh_callback()
    
    button_frame = ttk.Frame(frame)
    button_frame.pack(fill='x')
    
    create_modern_button(button_frame, "Update Task", perform_edit, 'Success.TButton').pack(side='right', padx=(5, 0))
    create_modern_button(button_frame, "Cancel", edit_win.destroy, 'Secondary.TButton').pack(side='right')

def delete_task_dialog(root, CURRENT_USER, tasks, refresh_callback):
    """Delete task dialog"""
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    if not CURRENT_USER:
        messagebox.showwarning("Warning", "🔒 Please log in first")
        return
        
    tid = simpledialog.askinteger("Delete Task", "Enter Task ID to delete:")
    if tid is None:
        return
        
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Error", "❌ Task not found")
        return
        
    if t["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Error", "🚫 You are not the owner of this task")
        return
        
    if messagebox.askyesno("Confirm Delete", 
                          f"Are you sure you want to delete task #{tid}?\n\"{t['title']}\"\n\nThis action cannot be undone."):
        tasks.delete_task(tid)
        messagebox.showinfo("Success", "🗑️ Task deleted successfully!")
        refresh_callback()