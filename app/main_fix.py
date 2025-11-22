from . import auth, tasks, fixed, storage, utils
from . import maintenance

def show_welcome():
    print("=================================================================")
    print(" ToDo CLI App — CWE-306 Demo (Fixed)")
    print("=================================================================")
    print()

def main_loop():
    auth.init_default_users()
    current_user = None
    while True:
        # Show welcome message
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
        # Only show Admin Tools when logged-in user is an admin
        if current_user and current_user.get("is_admin"):
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

        if action == "login":
            username = input("Username: ").strip()
            password = utils.prompt_hidden("Password: ")
            user = auth.login_user(username, password)
            if user:
                print(f"Logged in as {user['username']}")
                current_user = user
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
            else:
                print("Registration failed (username may exist).")

        elif action == "admin":
            # require an authenticated admin before showing admin tools (menu shown only for admins)
            admin = current_user
            if not admin:
                print("Admin authentication required.")

                # force login for admin access
                username = input("Admin username: ").strip()
                password = utils.prompt_hidden("Admin password: ")
                admin = auth.login_user(username, password)
                if not admin:
                    print("Authentication failed. Cannot access Admin Tools.")
                    continue
            if not admin.get("is_admin"):
                print("User is not an admin. Access denied.")
                continue

            # if admin authenticated, show admin tools menu
            while True:
                print("\n=== ADMIN TOOLS ===")
                print("1) Admin menu")
                print("2) Maintenance")
                print("3) Back")
                a = input("> ").strip()

                # go to admin menu for the to do lists and users management
                if a == "1":
                    fixed.admin_menu_interactive()

                # simple maintenance for user/ list checks
                elif a == "2":
                    maintenance.menu(admin)

                # go back to main menu
                elif a == "3":
                    break
                else:
                    print("Invalid choice.")

        elif action == "use":
            user_menu(current_user)

        elif action == "quit":
            print("Goodbye.")
            return

# user operations menu
def user_menu(current_user):
    # check for logged in user
    if not current_user:
        print("You are not logged in. Please login or register first.")
        return
    
    while True:
        print(f"\nUser Menu — logged in as {current_user['username']}")
        #print possible user actions
        print("1) Create task")
        print("2) List my tasks")
        print("3) Complete my task")
        print("4) Edit my task")
        print("5) Delete my task")
        print("6) Logout")
        print("7) Back to main menu")
        choice = input("> ").strip()

        # create a new task, runs through required fields user needs to input
        if choice == "1":
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            t = tasks.add_task(current_user['id'], title, desc)
            print(f"Created task id={t['id']}")

        # list my tasks, updates the text box on menu with current user's tasks
        elif choice == "2":
            # retrieve tasks for current user from the json storage which acts as a database
            my_tasks = tasks.list_tasks_for_user(current_user['id'])

            # check if user has any tasks
            if not my_tasks:
                # no tasks printed to box
                print("(no tasks)")
            else:
                # print each task with its details
                print("\nMy Tasks:")
                for t in my_tasks:
                    # print each task with its details in specified format, iterate for all tasks present in json for user
                    status = "✓" if t.get("done") else " "
                    title = t.get("title", "<no title>")
                    desc = t.get("description", "").strip()
                    created = t.get("created_at", "unknown")
                    print(f"- id={t.get('id')}  [{status}] {title}")
                    if desc:
                        print(f"    desc: {desc}")
                    print(f"    created: {created}")
        # quicker than using edit task, mark a task as complete by imputting its ID
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
            # technically not part of CWE-306 but important check to ensure user can only modify their own tasks
            if t['owner_id'] != current_user['id']:
                print("You are not the owner of this task.")
                continue
            tasks.update_task(tid, done=True)
            print("Task marked complete.")
        
        # edit a task's title and/or description by inputting its ID
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

        # logout user
        elif choice == "6":
            print(f"User {current_user['username']} logged out.")
            current_user.clear()
            return
        
        # go back to main menu
        elif choice == "7":
            return
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()