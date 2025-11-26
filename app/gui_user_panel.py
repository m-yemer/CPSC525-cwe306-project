'''
Professional task management panel
'''

# Track open windows
_open_windows = {}

def refresh_user_tasks_display(user_tasks_text, CURRENT_USER, tasks_module, COLORS):
    """Refresh task display with professional formatting"""
    import tkinter as tk
    from tkinter import ttk
    
    if not user_tasks_text or not hasattr(user_tasks_text, 'winfo_exists') or not user_tasks_text.winfo_exists():
        return
        
    user_tasks_text.config(state=tk.NORMAL)
    user_tasks_text.delete("1.0", tk.END)
    
    if not CURRENT_USER:
        user_tasks_text.insert(tk.END, "Please log in to view your tasks.\n\n", "center")
        user_tasks_text.insert(tk.END, "Use the Login button in the main window to access your tasks.", "hint")
    else:
        my_tasks = tasks_module.list_tasks_for_user(CURRENT_USER["id"])
        if not my_tasks:
            user_tasks_text.insert(tk.END, "No tasks found.\n\n", "center")
            user_tasks_text.insert(tk.END, "Click 'Create Task' to add your first task.", "hint")
        else:
            # Header
            user_tasks_text.insert(tk.END, f"Your Tasks ({len(my_tasks)} total):\n\n", "header")
            
            for t in my_tasks:
                status_icon = "[COMPLETED]" if t.get("done") else "[PENDING]"
                status_color = "completed" if t.get("done") else "pending"
                
                user_tasks_text.insert(tk.END, f"{status_icon} ", status_color)
                user_tasks_text.insert(tk.END, f"Task #{t.get('id')}: {t.get('title')}\n", "title")
                
                if t.get('description'):
                    user_tasks_text.insert(tk.END, f"    Description: {t.get('description','')}\n", "normal")
                
                user_tasks_text.insert(tk.END, f"    Created: {t.get('created_at','')}\n", "date")
                user_tasks_text.insert(tk.END, "\n", "spacer")
    
    # Configure text tags for professional styling
    user_tasks_text.tag_configure("center", justify='center', foreground=COLORS['text_secondary'])
    user_tasks_text.tag_configure("hint", justify='center', foreground=COLORS['text_secondary'], font=('Arial', 9))
    user_tasks_text.tag_configure("header", foreground=COLORS['primary'], font=('Arial', 11, 'bold'))
    user_tasks_text.tag_configure("title", foreground=COLORS['text_primary'], font=('Arial', 10, 'bold'))
    user_tasks_text.tag_configure("normal", foreground=COLORS['text_primary'], font=('Arial', 10))
    user_tasks_text.tag_configure("date", foreground=COLORS['text_secondary'], font=('Arial', 9))
    user_tasks_text.tag_configure("completed", foreground=COLORS['success'], font=('Arial', 10, 'bold'))
    user_tasks_text.tag_configure("pending", foreground=COLORS['warning'], font=('Arial', 10, 'bold'))
    user_tasks_text.tag_configure("spacer", font=('Arial', 4))
    
    user_tasks_text.config(state=tk.DISABLED)

def open_user_panel(root, CURRENT_USER, tasks_module, refresh_callback):
    """Professional user panel with task management"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button, create_scrolled_text, COLORS
    from .gui_components import create_header, center_window, create_section_label
    
    # Check authentication
    if not CURRENT_USER:
        messagebox.showwarning("Access Required", "Please log in to access the Task Manager.")
        return None, None
        
    # Prevent multiple user panels
    if 'user_panel' in _open_windows and _open_windows['user_panel'].winfo_exists():
        _open_windows['user_panel'].lift()
        return _open_windows['user_panel'], _open_windows.get('user_tasks_text')
        
    user_win = tk.Toplevel(root)
    _open_windows['user_panel'] = user_win
    user_win.title("Task Manager - TodoApp")
    user_win.geometry("900x650")
    user_win.minsize(800, 500)
    
    # Header
    header_frame = create_header(user_win, "Task Management", 
                               f"Managing tasks for: {CURRENT_USER['username']}")
    
    # Action buttons toolbar
    toolbar_frame = create_modern_frame(user_win, 15)
    toolbar_frame.pack(fill='x', padx=40, pady=(0, 20))
    
    create_modern_button(toolbar_frame, "Create Task", 
                        lambda: create_task_dialog(user_win, CURRENT_USER, tasks_module, refresh_callback), 
                        'Success.TButton', 16).grid(row=0, column=0, padx=6, pady=6)
    create_modern_button(toolbar_frame, "Complete Task", 
                        lambda: complete_task_dialog(user_win, CURRENT_USER, tasks_module, refresh_callback), 
                        'Primary.TButton', 16).grid(row=0, column=1, padx=6, pady=6)
    create_modern_button(toolbar_frame, "Edit Task", 
                        lambda: edit_task_dialog(user_win, CURRENT_USER, tasks_module, refresh_callback), 
                        'Secondary.TButton', 16).grid(row=0, column=2, padx=6, pady=6)
    create_modern_button(toolbar_frame, "Delete Task", 
                        lambda: delete_task_dialog(user_win, CURRENT_USER, tasks_module, refresh_callback), 
                        'Danger.TButton', 16).grid(row=0, column=3, padx=6, pady=6)
    create_modern_button(toolbar_frame, "Refresh", 
                        refresh_callback, 
                        'Secondary.TButton', 16).grid(row=0, column=4, padx=6, pady=6)
    
    # Tasks display area
    content_frame = create_modern_frame(user_win, 20)
    content_frame.pack(fill='both', expand=True, padx=40, pady=10)
    
    create_section_label(content_frame, "Your Tasks").pack(anchor='w', pady=(0, 12))
    
    user_tasks_text = create_scrolled_text(content_frame, width=85, height=22)
    user_tasks_text.pack(fill='both', expand=True)
    
    _open_windows['user_tasks_text'] = user_tasks_text
    
    def cleanup():
        """Clean up window tracking"""
        _open_windows.pop('user_panel', None)
        _open_windows.pop('user_tasks_text', None)
        user_win.destroy()
    
    user_win.protocol("WM_DELETE_WINDOW", cleanup)
    center_window(user_win)
    
    return user_win, user_tasks_text

def create_task_dialog(parent, CURRENT_USER, tasks_module, refresh_callback):
    """Professional task creation dialog"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    from .gui_styles import create_modern_frame, create_modern_button
    from .gui_components import center_window, create_dialog_header, create_form_field
    
    create_win = tk.Toplevel(parent)
    create_win.title("Create New Task")
    create_win.geometry("500x400")
    create_win.resizable(False, False)
    create_win.transient(parent)
    create_win.grab_set()
    
    main_frame = create_modern_frame(create_win, 25)
    main_frame.pack(fill='both', expand=True)
    
    create_dialog_header(main_frame, "Create New Task")
    
    # Form fields
    title_var, title_entry = create_form_field(main_frame, "Task Title *", 'entry', '', 30)
    
    # Description (multi-line)
    desc_frame = ttk.Frame(main_frame)
    desc_frame.pack(fill='x', pady=12)
    
    ttk.Label(desc_frame, text="Description:", style='Header.TLabel').pack(anchor='w', pady=(0, 5))
    desc_text = tk.Text(desc_frame, width=50, height=8, font=('Arial', 10), wrap='word')
    desc_text.pack(fill='both')
    
    # Focus title field
    title_entry.focus()
    
    creation_in_progress = False
    
    def perform_create():
        nonlocal creation_in_progress
        if creation_in_progress:
            return
            
        title = title_var.get().strip()
        description = desc_text.get("1.0", tk.END).strip()
        
        # Validation
        if not title:
            messagebox.showerror("Input Error", "Task title is required.")
            title_entry.focus()
            return
        
        if len(title) < 2:
            messagebox.showerror("Input Error", "Task title must be at least 2 characters long.")
            title_entry.focus()
            return
        
        # Disable UI during creation
        creation_in_progress = True
        create_btn.config(state='disabled')
        cancel_btn.config(state='disabled')
        
        try:
            # Create task
            task = tasks_module.add_task(CURRENT_USER["id"], title, description)
            messagebox.showinfo("Success", f"Task created successfully!\n\nTask ID: {task['id']}\nTitle: {task['title']}")
            create_win.destroy()
            refresh_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create task: {str(e)}")
        finally:
            # Re-enable UI
            creation_in_progress = False
            create_btn.config(state='normal')
            cancel_btn.config(state='normal')
    
    # Buttons
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill='x', pady=(20, 0))
    
    create_btn = create_modern_button(button_frame, "Create Task", perform_create, 'Success.TButton')
    create_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = create_modern_button(button_frame, "Cancel", create_win.destroy, 'Secondary.TButton')
    cancel_btn.pack(side='right')
    
    # Bind Enter key to create
    title_entry.bind('<Return>', lambda e: perform_create())
    
    center_window(create_win)

def complete_task_dialog(parent, CURRENT_USER, tasks_module, refresh_callback):
    """Complete task dialog"""
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    task_id = simpledialog.askinteger("Complete Task", 
                                    "Enter the ID of the task to mark as complete:",
                                    parent=parent,
                                    minvalue=1)
    
    if not task_id:
        return
    
    task = tasks_module.get_task(task_id)
    if not task:
        messagebox.showerror("Error", f"Task with ID {task_id} not found.")
        return
    
    if task["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Access Denied", "You can only complete your own tasks.")
        return
    
    # Confirm completion
    if messagebox.askyesno("Confirm Completion", 
                          f"Mark task as complete?\n\nTitle: {task['title']}"):
        tasks_module.update_task(task_id, done=True)
        messagebox.showinfo("Success", "Task marked as complete.")
        refresh_callback()

def edit_task_dialog(parent, CURRENT_USER, tasks_module, refresh_callback):
    """Edit task dialog"""
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    task_id = simpledialog.askinteger("Edit Task", 
                                    "Enter the ID of the task to edit:",
                                    parent=parent,
                                    minvalue=1)
    
    if not task_id:
        return
    
    task = tasks_module.get_task(task_id)
    if not task:
        messagebox.showerror("Error", f"Task with ID {task_id} not found.")
        return
    
    if task["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Access Denied", "You can only edit your own tasks.")
        return
    
    # For now, use a simple dialog - could be enhanced with a full edit form
    new_title = simpledialog.askstring("Edit Task", 
                                     f"New title for task (current: {task['title']}):",
                                     parent=parent,
                                     initialvalue=task['title'])
    
    if new_title is not None:
        tasks_module.update_task(task_id, title=new_title.strip())
        messagebox.showinfo("Success", "Task updated successfully.")
        refresh_callback()

def delete_task_dialog(parent, CURRENT_USER, tasks_module, refresh_callback):
    """Delete task dialog"""
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    task_id = simpledialog.askinteger("Delete Task", 
                                    "Enter the ID of the task to delete:",
                                    parent=parent,
                                    minvalue=1)
    
    if not task_id:
        return
    
    task = tasks_module.get_task(task_id)
    if not task:
        messagebox.showerror("Error", f"Task with ID {task_id} not found.")
        return
    
    if task["owner_id"] != CURRENT_USER["id"]:
        messagebox.showerror("Access Denied", "You can only delete your own tasks.")
        return
    
    # Confirm deletion
    if messagebox.askyesno("Confirm Deletion", 
                          f"Permanently delete this task?\n\n"
                          f"ID: {task['id']}\n"
                          f"Title: {task['title']}\n\n"
                          f"This action cannot be undone."):
        tasks_module.delete_task(task_id)
        messagebox.showinfo("Success", "Task deleted successfully.")
        refresh_callback()