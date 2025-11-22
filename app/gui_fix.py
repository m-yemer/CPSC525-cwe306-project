'''
THis is the GUI implementation of the app, works off the CLI implementation
'''

import tkinter as tk # GUI framework used
from tkinter import simpledialog, messagebox, scrolledtext
from . import auth, tasks, vulnerable, fixed, storage, utils, maintenance

# global variables
CURRENT_USER = None
user_win = None
user_tasks_text = None
admin_win = None

def set_user_label(lbl):
    # set the user label
    lbl.config(text=f"User: {CURRENT_USER['username']}" if CURRENT_USER else "User: (not logged in)")

def login(lbl):
    # login dialog 
    global CURRENT_USER
    username = simpledialog.askstring("Login", "Username:") # ask for username
    if not username:
        return
    password = simpledialog.askstring("Login", "Password:", show="*") #ask for password
    user = auth.login_user(username, password) #authenticate
    if user:
        CURRENT_USER = user # set global user as logged in user
        set_user_label(lbl)
        messagebox.showinfo("Login", f"Logged in as {user['username']}")
    else:
        # login failure
        messagebox.showerror("Login", "Login failed")

def logout():
    # logout current user
    global CURRENT_USER
    if not CURRENT_USER:
        return
    uname = CURRENT_USER.get("username")
    CURRENT_USER = None
    messagebox.showinfo("Logout", f"User {uname} logged out.")

def register():
    #register user dialog box
    username = simpledialog.askstring("Register", "Choose username:")
    if not username:
        return
    password = simpledialog.askstring("Register", "Choose password:", show="*")

    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        #if the current user is admin, give them the option create new admin
        make_admin = messagebox.askyesno("Register", "Make this user admin?")
        u = auth.register_user(username, password, is_admin=make_admin)
    else:
        # register anyone can use to make generaal account
        u = auth.register_user(username, password)
    if u:
        # sucessful register
        messagebox.showinfo("Register", f"Registered {username}")
    else:
        # error
        messagebox.showerror("Register", "Registration failed (username may exist)")

def open_user_panel():
    # open user panel window
    global user_win, user_tasks_text
    if user_win and tk.Toplevel.winfo_exists(user_win):
        user_win.lift() #put window frunt
        return
    user_win = tk.Toplevel(root)
    user_win.title("User Panel")
    frm = tk.Frame(user_win)
    frm.pack(padx=8, pady=8)

    # action buttons for task management
    tk.Button(frm, text="Create Task", width=18, command=create_task).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frm, text="Complete Task", width=18, command=complete_task).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(frm, text="Delete Task", width=18, command=delete_task).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="Refresh Tasks", width=18, command=refresh_user_tasks).grid(row=1, column=1, padx=4, pady=4)

    # text area for displaying tasks
    user_tasks_text = scrolledtext.ScrolledText(user_win, width=80, height=20)
    user_tasks_text.pack(padx=8, pady=(4,8))
    refresh_user_tasks() # load tasks

def refresh_user_tasks():
    # refresh the task display for the user
    global user_tasks_text
    if not user_tasks_text:
        return
    user_tasks_text.config(state=tk.NORMAL)
    user_tasks_text.delete("1.0", tk.END) # clear existing text


    if not CURRENT_USER:
        user_tasks_text.insert(tk.END, "(not logged in)\n") # lgin prompt
    else:
        my_tasks = tasks.list_tasks_for_user(CURRENT_USER["id"])
        if not my_tasks:
            user_tasks_text.insert(tk.END, "(no tasks)\n")
        else:
            for t in my_tasks:
                # show task details
                user_tasks_text.insert(tk.END, f"id={t.get('id')}  title={t.get('title')}  done={t.get('done')}\n")
                user_tasks_text.insert(tk.END, f"  desc: {t.get('description','')}\n")
                user_tasks_text.insert(tk.END, f"  created: {t.get('created_at','')}\n\n")
    user_tasks_text.config(state=tk.DISABLED)

def create_task():
    # create new task process
    # just gives windows to input required info to make new task
    if not CURRENT_USER:
        messagebox.showwarning("Create", "Please login first")
        return
    title = simpledialog.askstring("Create Task", "Title:")
    if title is None:
        return
    desc = simpledialog.askstring("Create Task", "Description:")
    t = tasks.add_task(CURRENT_USER["id"], title, desc or "")
    messagebox.showinfo("Create", f"Created task id={t['id']}")
    refresh_user_tasks()

def complete_task():
    # mark task as complete
    if not CURRENT_USER:
        messagebox.showwarning("Complete", "Please login first")
        return
    
    #get task id
    tid = simpledialog.askinteger("Complete Task", "Task id to mark complete:")
    if tid is None:
        return
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Complete", "Task not found")
        return
    if t["owner_id"] != CURRENT_USER["id"]:
        #check if task belongs to user
        messagebox.showerror("Complete", "You are not the owner of this task")
        return
    tasks.update_task(tid, done=True)
    messagebox.showinfo("Complete", "Task marked complete")
    refresh_user_tasks()

def delete_task():
    # delete individual task
    if not CURRENT_USER:
        messagebox.showwarning("Delete", "Please login first")
        return
    tid = simpledialog.askinteger("Delete Task", "Task id to delete:")
    if tid is None:
        return
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Delete", "Task not found")
        return
    if t["owner_id"] != CURRENT_USER["id"]:
        #check user owns the tasks
        messagebox.showerror("Delete", "You are not the owner of this task")
        return
    tasks.delete_task(tid)
    messagebox.showinfo("Delete", "Task deleted")
    refresh_user_tasks()

def admin_tools():
    global admin_win
    # Authenticate admin first 
    admin = CURRENT_USER
    if not admin or not admin.get("is_admin"):
        # if not already admin, request creadentials
        username = simpledialog.askstring("Admin Auth", "Admin username:")
        if not username:
            return
        password = simpledialog.askstring("Admin Auth", "Admin password:", show="*")
        admin = auth.login_user(username, password) # authenticate user
        if not admin:
            # general fail
            messagebox.showerror("Admin", "Authentication failed. Cannot open Admin Tools.")
            return
        if not admin.get("is_admin"):
            # user credneital not belonging to admin
            messagebox.showerror("Admin", "User is not an admin. Access denied.")
            return

    if admin_win and tk.Toplevel.winfo_exists(admin_win):
        admin_win.lift()
        return
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Tools (Fixed - authenticated)")
    frm = tk.Frame(admin_win)
    frm.pack(padx=8, pady=8)

    # button to open admin functions
    tk.Button(frm, text="1) Admin menu",
               width=36, command=lambda: admin_menu(admin)).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frm, text="2) Maintenance ", width=36, command=lambda: open_maintenance_window(admin)).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="3) Back", width=36, command=admin_win.destroy).grid(row=2, column=0, padx=4, pady=8)

def admin_menu(admin):
    # interactive admin menu for authenticated admin

    sub = tk.Toplevel(root)
    sub.title("=== ADMIN TOOLS === (authenticated)")
    frame = tk.Frame(sub)
    frame.pack(padx=8, pady=8)

    task_display = scrolledtext.ScrolledText(sub, width=80, height=20)
    task_display.pack(padx=8, pady=(4,8))
    task_display.config(state=tk.DISABLED)

    def do_delete_all_fixed():
        # the main vulnerability here is fixed, only accessible if user account
        if not messagebox.askyesno("Confirm", "Delete ALL tasks for all users?"):

            return
        try:
            if hasattr(fixed, "delete_all_tasks_fixed"):
                ok = fixed.delete_all_tasks_fixed(admin) # calls the fixed delete all tool, only works if user is an admin
                if ok:
                    messagebox.showinfo("Admin", "All tasks deleted ")
                else:
                    messagebox.showerror("Admin", "Delete failed (not authorized)")
            else:
                storage.save_tasks([])
                storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={admin['id']}")
                messagebox.showinfo("Admin", "All tasks deleted (fixed fallback)")
        except Exception as e:
            messagebox.showerror("Admin", f"Delete failed: {e}")
        refresh_user_tasks()
        refresh_view()

    def refresh_view():
        # refresh task display
        tasks_all = storage.load_tasks() or []
        task_display.config(state=tk.NORMAL)
        task_display.delete("1.0", tk.END)
        if not tasks_all:
            task_display.insert(tk.END, "(no tasks)\n")
        else:
            for t in tasks_all:
                task_display.insert(tk.END, f"id={t.get('id')} owner={t.get('owner_id')} title={t.get('title')} done={t.get('done')}\n")
                task_display.insert(tk.END, f"  desc: {t.get('description','')}\n")
                task_display.insert(tk.END, f"  created: {t.get('created_at','')}\n\n")
        task_display.config(state=tk.DISABLED)

    tk.Button(frame, text="Delete ALL tasks (authorized)", width=36, fg="red", command=do_delete_all_fixed).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frame, text="View ALL tasks", width=36, command=refresh_view).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frame, text="Back", width=36, command=sub.destroy).grid(row=2, column=0, padx=4, pady=8)

    refresh_view()


def open_maintenance_window(admin):
    # maintenance window
    
    win = tk.Toplevel(root)
    win.title("Maintenance")
    frm = tk.Frame(win)
    frm.pack(padx=8, pady=8)

    out = scrolledtext.ScrolledText(win, width=80, height=16)
    out.pack(padx=8, pady=(4,8))
    out.config(state=tk.DISABLED)

    def show_stats():
        # show stats which just general info on users and tasks
        s = maintenance.stats()
        out.config(state=tk.NORMAL)
        out.delete("1.0", tk.END)
        out.insert(tk.END, f"{s}\n")
        out.config(state=tk.DISABLED)

    def do_backup():
        # only require admin status for backup
        if not admin or not admin.get("is_admin"):
            messagebox.showerror("Maintenance", "Admin required for backup")
            return
        p = maintenance.backup_data()
        messagebox.showinfo("Backup", f"Backup created: {p}")

    def do_restore():
        # only require admin status for restore
        if not admin or not admin.get("is_admin"):
            messagebox.showerror("Maintenance", "Admin required for restore")
            return
        name = simpledialog.askstring("Restore", "Backup name or dir:")
        if not name:
            return
        ok = maintenance.restore_backup(name)
        messagebox.showinfo("Restore", "Restore succeeded." if ok else "Restore failed.")

    def do_generate():
        # generate sample data fro tasks and users
        # mainly just meant for demo purposes
        u = simpledialog.askstring("Generate", "Additional users to create (default 10):")
        t = simpledialog.askstring("Generate", "Tasks per user (default 10):")
        try:
            nu = int(u) if u else 10
            nt = int(t) if t else 10
        except ValueError:
            messagebox.showerror("Generate", "Invalid numbers")
            return
        res = maintenance.generate_sample_data(nu, nt)
        messagebox.showinfo("Generate", f"Generated {res['created_users']} users and {res['created_tasks']} tasks.")

    tk.Button(frm, text="Show stats", width=20, command=show_stats).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frm, text="Backup data (admin)", width=20, command=do_backup).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(frm, text="Restore from backup (admin)", width=20, command=do_restore).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="Generate sample data", width=20, command=do_generate).grid(row=1, column=1, padx=4, pady=4)
    tk.Button(frm, text="Close", width=44, command=win.destroy).grid(row=2, column=0, columnspan=2, pady=8)





def quit_app():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ToDo App — Fixed GUI")
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    user_lbl = tk.Label(main_frame, text="User: (not logged in)")
    user_lbl.grid(row=0, column=0, columnspan=2, sticky="w")
    set_user_label(user_lbl)

    def refresh_main_menu():
        # remove all widgets except user label
        for widget in main_frame.winfo_children():
            if widget != user_lbl:
                widget.destroy()
        set_user_label(user_lbl)
        # recreate buttons
 
        # show Login or Logout 
        if not CURRENT_USER:
            tk.Button(main_frame, text="Login", width=18, command=lambda: [login(user_lbl), refresh_main_menu()]).grid(row=1, column=0, padx=4, pady=4)
        else:
            tk.Button(main_frame, text="Logout", width=18, command=lambda: [logout(), refresh_main_menu()]).grid(row=1, column=0, padx=4, pady=4)


        tk.Button(main_frame, text="Register", width=18, command=lambda: [register(), refresh_main_menu()]).grid(row=1, column=1, padx=4, pady=4)

        if CURRENT_USER and CURRENT_USER.get("is_admin"):
            tk.Button(main_frame, text="Admin Tools", width=18, command=admin_tools).grid(row=2, column=0, padx=4, pady=4)
        tk.Button(main_frame, text="Use App", width=18, command=open_user_panel).grid(row=2, column=1, padx=4, pady=4)
        tk.Button(main_frame, text="Quit", width=38, command=quit_app).grid(row=3, column=0, columnspan=2, pady=8)

    refresh_main_menu()
    root.mainloop()