import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from . import auth, tasks, vulnerable, storage, utils, maintenance

# global variables
CURRENT_USER = None
user_win = None
user_tasks_text = None
admin_win = None

def set_user_label(lbl):
    # set user label header
    lbl.config(text=f"User: {CURRENT_USER['username']}" if CURRENT_USER else "User: (not logged in)")

def login(lbl):
    # login dialog windows
    global CURRENT_USER
    username = simpledialog.askstring("Login", "Username:") # get username
    if not username:
        return
    password = simpledialog.askstring("Login", "Password:", show="*") # get password
    user = auth.login_user(username, password) # authenticate
    if user:
        # sucess
        CURRENT_USER = user
        set_user_label(lbl)
        messagebox.showinfo("Login", f"Logged in as {user['username']}")
    else:
        # error
        messagebox.showerror("Login", "Login failed")

def register():
    # register a new user
    username = simpledialog.askstring("Register", "Choose username:")
    if not username:
        return
    password = simpledialog.askstring("Register", "Choose password:", show="*")
    
    if CURRENT_USER and CURRENT_USER.get("is_admin"):
        # user can only make ne wuser admin if they are an admin 
        # (wasnt sure if i should add this due to CWE306, but maintenance and
        # admin tools probably enough for demo)
        make_admin = messagebox.askyesno("Register", "Make this user admin?")
        u = auth.register_user(username, password, is_admin=make_admin)
    else:
        # general user register
        u = auth.register_user(username, password)
    if u:
        #sucess
        messagebox.showinfo("Register", f"Registered {username}")
    else:
        #failure
        messagebox.showerror("Register", "Registration failed (username may exist)")

def open_user_panel():
    # open user panel window
    global user_win, user_tasks_text
    if user_win and tk.Toplevel.winfo_exists(user_win):
        user_win.lift()
        return
    user_win = tk.Toplevel(root)
    user_win.title("User Panel")
    frm = tk.Frame(user_win)
    frm.pack(padx=8, pady=8)

    # buttons for user action
    tk.Button(frm, text="Create Task", width=18, command=create_task).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frm, text="Complete Task", width=18, command=complete_task).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(frm, text="Delete Task", width=18, command=delete_task).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="Refresh Tasks", width=18, command=refresh_user_tasks).grid(row=1, column=1, padx=4, pady=4)
    user_tasks_text = scrolledtext.ScrolledText(user_win, width=80, height=20)
    user_tasks_text.pack(padx=8, pady=(4,8))
    refresh_user_tasks()

def refresh_user_tasks():
    #refresh the task list for the current user
    # keep it clean and consistent for what user does
    global user_tasks_text
    if not user_tasks_text:
        return
    user_tasks_text.config(state=tk.NORMAL)
    user_tasks_text.delete("1.0", tk.END)
    if not CURRENT_USER:
        user_tasks_text.insert(tk.END, "(not logged in)\n")
    else:
        my_tasks = tasks.list_tasks_for_user(CURRENT_USER["id"])
        if not my_tasks:
            user_tasks_text.insert(tk.END, "(no tasks)\n") # clear
        else:
            for t in my_tasks:
                # format to display each task
                user_tasks_text.insert(tk.END, f"id={t.get('id')}  title={t.get('title')}  done={t.get('done')}\n")
                user_tasks_text.insert(tk.END, f"  desc: {t.get('description','')}\n")
                user_tasks_text.insert(tk.END, f"  created: {t.get('created_at','')}\n\n")
    user_tasks_text.config(state=tk.DISABLED)

def create_task():
    #allow user to add task
    if not CURRENT_USER:
        messagebox.showwarning("Create", "Please login first")
        return
    # ask user to input required fields to save task
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
    tid = simpledialog.askinteger("Complete Task", "Task id to mark complete:")
    if tid is None:
        # tid doesnt exist
        return
    t = tasks.get_task(tid)
    if not t:
        messagebox.showerror("Complete", "Task not found")
        return
    if t["owner_id"] != CURRENT_USER["id"]:
        # check user not owner
        # again wasnt sure to authenticate or not here 
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
    tid = simpledialog.askinteger("Delete Task", "Task id to delete:") # ask task id
    if tid is None:
        return
    t = tasks.get_task(tid)
    if not t:
        # taks doesnt exist
        messagebox.showerror("Delete", "Task not found")
        return
    if t["owner_id"] != CURRENT_USER["id"]:
        # check user logged in is owner (not sure to authent)
        messagebox.showerror("Delete", "You are not the owner of this task")
        return
    tasks.delete_task(tid)
    messagebox.showinfo("Delete", "Task deleted")
    refresh_user_tasks()

def admin_tools():
    # MAIN VULNERABILITY
    # access to admin tools without authentification check
    global admin_win
    if admin_win and tk.Toplevel.winfo_exists(admin_win):
        admin_win.lift()
        return
    admin_win = tk.Toplevel(root)
    admin_win.title("Admin Tools ")
    frm = tk.Frame(admin_win)
    frm.pack(padx=8, pady=8)

    # matches CLI options
    tk.Button(frm, text="1) Vulnerable admin menu", width=36, command=admin_menu).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frm, text="2) Maintenance", width=36, command=lambda: open_maintenance_window({"id":0,"username":"unauth","is_admin":True})).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="3) Back", width=36, command=admin_win.destroy).grid(row=2, column=0, padx=4, pady=8)

def admin_menu():
    #open admin window not authenitfication here
    sub = tk.Toplevel(root)
    sub.title("=== ADMIN TOOLS ===")
    frame = tk.Frame(sub)
    frame.pack(padx=8, pady=8)

    # area to show task list for option 2
    task_display = scrolledtext.ScrolledText(sub, width=80, height=20)
    task_display.pack(padx=8, pady=(4,8))
    task_display.config(state=tk.DISABLED)

    def do_delete_all():
        # major vulnerability here
        # just allow any user to delete the entire task database
        if not messagebox.askyesno("Confirm", "Delete ALL tasks for all users?"):
            return
        # vulnerable delete
        try:
            vulnerable.delete_all_tasks()
            messagebox.showinfo("Admin", "All tasks deleted ")
        except Exception as e:
            messagebox.showerror("Admin", f"Delete failed: {e}")
        refresh_user_tasks()
        refresh_view()

    def refresh_view():
        # show all tasks in window
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

    tk.Button(frame, text="Delete ALL tasks ", width=36, fg="red", command=do_delete_all).grid(row=0, column=0, padx=4, pady=4)
    tk.Button(frame, text="View ALL tasks", width=36, command=refresh_view).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frame, text="Back", width=36, command=sub.destroy).grid(row=2, column=0, padx=4, pady=8)

    # initial populate
    refresh_view()


def open_maintenance_window(current_user):
    # secondary authentification problem (CWE-306)

    win = tk.Toplevel(root)
    win.title("Maintenance")
    frm = tk.Frame(win)
    frm.pack(padx=8, pady=8)

    out = scrolledtext.ScrolledText(win, width=80, height=16)
    out.pack(padx=8, pady=(4,8))
    out.config(state=tk.DISABLED)

    def show_stats():
        # any user can see the tasks of all other users
        # privacy issue
        s = maintenance.stats()
        out.config(state=tk.NORMAL)
        out.delete("1.0", tk.END)
        out.insert(tk.END, f"{s}\n")
        out.config(state=tk.DISABLED)

    def do_backup():
        # vulnerable GUI may allow backup without proper authentification
        # can save other users task data
        p = maintenance.backup_data()
        messagebox.showinfo("Backup", f"Backup created: {p}")

    def do_restore():
        # can put their own backup with authentification
        name = simpledialog.askstring("Restore", "Backup name or dir:")
        if not name:
            return
        ok = maintenance.restore_backup(name)
        messagebox.showinfo("Restore", "Restore succeeded." if ok else "Restore failed.")

    def do_generate():
        # in maintenance but technically for demo purposes
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
    tk.Button(frm, text="Backup data", width=20, command=do_backup).grid(row=0, column=1, padx=4, pady=4)
    tk.Button(frm, text="Restore from backup", width=20, command=do_restore).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(frm, text="Generate sample data", width=20, command=do_generate).grid(row=1, column=1, padx=4, pady=4)
    tk.Button(frm, text="Close", width=44, command=win.destroy).grid(row=2, column=0, columnspan=2, pady=8)

def quit_app():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ToDo App — Vulnerable GUI")
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10)

    # main menu buttons
    user_lbl = tk.Label(main_frame, text="User: (not logged in)")
    user_lbl.grid(row=0, column=0, columnspan=2, sticky="w")
    set_user_label(user_lbl)

    tk.Button(main_frame, text="Login", width=18, command=lambda: login(user_lbl)).grid(row=1, column=0, padx=4, pady=4)
    tk.Button(main_frame, text="Register", width=18, command=register).grid(row=1, column=1, padx=4, pady=4)
    tk.Button(main_frame, text="Admin Tools", width=18, command=admin_tools).grid(row=2, column=0, padx=4, pady=4)
    tk.Button(main_frame, text="Use App", width=18, command=open_user_panel).grid(row=2, column=1, padx=4, pady=4)
    tk.Button(main_frame, text="Quit", width=38, command=quit_app).grid(row=3, column=0, columnspan=2, pady=8)

    root.mainloop()