from . import auth, tasks, vulnerable, storage, utils
from . import maintenance
from .session import AuthenticatedAdminSession

def show_welcome():
    print("=================================================================")
    print(" ToDo CLI App — CWE-306 Demo (Vulnerability Present)")
    print("=================================================================")
    print()

def main_loop():
    auth.init_default_users()
    current_user = None
    admin_session = None
    while True:
        show_welcome()

        # dynamic menu entries
        entries = []
        labels = {
            "login": "Login",
            "register": "Register",
            "admin": "Admin Tools",
            "use": "Use App (user features)",
            "quit": "Quit",
        }

        entries.append("login")
        entries.append("register")
        # only show admin tools if logged in user is an admin 
        if current_user and current_user.get("is_admin"):
            # only show Admin Tools if we have a valid admin session
            if admin_session and isinstance(admin_session, AuthenticatedAdminSession) and admin_session.is_valid():
                entries.append("admin")
        entries.append("use")
        entries.append("quit")

        print("Main Menu:")
        for i, e in enumerate(entries, start=1):
            print(f"{i}) {labels[e]}")

        choice = input("> ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(entries):
            print("Invalid choice. Try again.")
            continue

        action = entries[int(choice) - 1]

        if action == "quit":
            print("Exiting. Goodbye!")
            break

        if action == "login":
            username = input("Username: ").strip()
            password = utils.prompt_hidden("Password: ")
            user = auth.login_user(username, password)
            if user:
                print(f"Logged in as {user['username']}")
                current_user = user
                # if admin create session
                if user.get("is_admin"):
                    admin_session = AuthenticatedAdminSession(user)
                else:
                    admin_session = None
                continue  # Show main menu again after login
            else:
                print("Login failed.")

        elif action == "register":
            username = input("Choose username: ").strip()
            password = utils.prompt_hidden("Choose password: ")

            if current_user and current_user.get("is_admin"):
                is_admin_answer = input("Make this user admin? (y/N): ").strip().lower()
                is_admin = is_admin_answer == "y"
                u = auth.register_user(username, password, is_admin=is_admin)
            else:
                u = auth.register_user(username, password)
            if u:
                print(f"Registered {username} (admin={u.get('is_admin', False)})")
                continue  # Show main menu again after registration
            else:
                print("Registration failed (username may exist).")

        elif action == "admin":
            # Admin tools (accessible only because menu only shows it for admins)
            while True:
                print("\n=== ADMIN TOOLS ===")
                print("1) Vulnerable admin menu")
                print("2) Maintenance ")
                print("3) Back")
                a = input("> ").strip()

                if a == "1":
                    vulnerable.admin_menu_interactive()
                elif a == "2":
                    admin_override = {"id": 0, "username": "unauth", "is_admin": True}
                    maintenance.menu(admin_override)
                elif a == "3":
                    break
                else:
                    print("Invalid choice.")
            continue  # After admin tools, show main menu again

        elif action == "admin":
            # require a valid AuthenticatedAdminSession for admin tools
            if not (admin_session and isinstance(admin_session, AuthenticatedAdminSession) and admin_session.is_valid()):
                print("Admin authentication required.")
                username = input("Admin username: ").strip()
                password = utils.prompt_hidden("Admin password: ")
                admin = auth.login_user(username, password)
                if admin and admin.get("is_admin"):
                    admin_session = AuthenticatedAdminSession(admin)
                else:
                    print("Admin authentication failed.")
                    continue
            # Admin tools (accessible only because menu only shows it for admins)
            while True:
                print("\n=== ADMIN TOOLS ===")
                print("1) Vulnerable admin menu")
                print("2) Maintenance ")
                print("3) Back")
                a = input("> ").strip()

                if a == "1":
                    vulnerable.admin_menu_interactive()
                elif a == "2":
                    maintenance.maintenance_menu()
                elif a == "3":
                    break
                else:
                    print("Invalid choice.")
        print("2) List my tasks")
        print("3) Complete my task")
        print("4) Edit my task")
        print("5) Delete my task")
        print("6) Logout")
        print("7) Back to main menu")
        choice = input("> ").strip()

        # create new task, runs through required fields user needs to input
        if choice == "1":
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            t = tasks.add_task(current_user['id'], title, desc)
            print(f"Created task id={t['id']}")

        # list all tasks for the logged in user
        elif choice == "2":
            my_tasks = tasks.list_tasks_for_user(current_user['id'])
            if not my_tasks:
                print("(no tasks)")
            else:
                print("\nMy Tasks:")
                for t in my_tasks:
                    status = "✓" if t.get("done") else " "
                    title = t.get("title", "<no title>")
                    desc = t.get("description", "").strip()
                    created = t.get("created_at", "unknown")
                    print(f"- id={t.get('id')}  [{status}] {title}")
                    if desc:
                        print(f"    desc: {desc}")
                    print(f"    created: {created}")

        # mark a task as complete by inputting its ID
        elif choice == "3":
            tid_raw = input("Task id to mark complete: ").strip()
            if not tid_raw.isdigit():
                print("Invalid id")
                continue
            tid = int(tid_raw)
            t = tasks.get_task(tid)
            if not t:
                print("Task not found")
                continue
            #--------------------------------------------
            # may change for the vuln file. added authn vulnerability here
            if t['owner_id'] != current_user['id']:
                print("You are not the owner of this task.")
                continue
            tasks.update_task(tid, done=True)
            print("Task marked complete.")

        # edit a task, change title and desc
        elif choice == "4":
            tid_raw = input("Task id to edit: ").strip()
            if not tid_raw.isdigit():
                print("Invalid id")
                continue
            tid = int(tid_raw)
            t = tasks.get_task(tid)
            if not t:
                print("Task not found")
                continue
            if t['owner_id'] != current_user['id']:
                print("You are not the owner of this task.")
                continue
            new_title = input(f"New title (blank to keep '{t['title']}'): ").strip()
            new_desc = input(f"New description (blank to keep current): ").strip()
            tasks.update_task(tid, title=(new_title or None), description=(new_desc or None))
            print("Task updated.")

        # delete a task by inputting its ID
        elif choice == "5":
            tid_raw = input("Task id to delete: ").strip()
            if not tid_raw.isdigit():
                print("Invalid id")
                continue
            tid = int(tid_raw)
            t = tasks.get_task(tid)
            if not t:
                print("Task not found.")
                continue
            if t['owner_id'] != current_user['id']:
                print("You are not the owner of this task.")
                continue
            tasks.delete_task(tid)
            print("Task deleted.")

        # logout
        elif choice == "6":
            print(f"User {current_user['username']} logged out.")
            current_user.clear()
            return
        elif choice == "7":
            continue
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()