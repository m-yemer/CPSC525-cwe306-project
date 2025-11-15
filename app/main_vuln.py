from . import auth, tasks, vulnerable, storage, utils
from . import maintenance

def show_welcome():
    print("=================================================================")
    print(" ToDo CLI App — CWE-306 Demo (Vulnerability Present)")
    print("=================================================================")
    print()

def main_loop():
    auth.init_default_users()
    current_user = None
    while True:
        show_welcome()
        print("Main Menu:")
        print("1) Login")
        print("2) Register")
        print("3) Admin Tools")   # intentionally exposed to all since there is not authentification check to access
        print("4) Use App (user features)")
        print("5) Quit")
        choice = input("> ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            password = utils.prompt_hidden("Password: ")
            user = auth.login_user(username, password)
            # attempt login
            if user:
                print(f"Logged in as {user['username']}")
                current_user = user
            else:
                print("Login failed.")

        # menue to register a new user
        elif choice == "2":
            username = input("Choose username: ").strip()
            password = utils.prompt_hidden("Choose password: ")
            u = auth.register_user(username, password)
            if u:
                print(f"Registered {username}")
            else:
                print("Registration failed (username may exist).")

        #---------------------------------
        # WEAKNESS HERE: No authentication required to access admin tools
        #---------------------------------
        elif choice == "3":
            
            # vulnerable access: admin tool menu accessible without auth
            while True:
                print("\n=== ADMIN TOOLS ===")
                print("1) Vulnerable admin menu")
                print("2) Maintenance ")
                print("3) Back")
                a = input("> ").strip()

                #go to menu for all users to do list and users management
                if a == "1":
                    vulnerable.admin_menu_interactive()

                # allow any user to access maintenance menu
                # can view personal tasks of all users and see logs
                elif a == "2":
                    admin_override = {"id": 0, "username": "unauth", "is_admin": True}
                    maintenance.menu(admin_override)
                
                # go back to main menu
                elif a == "3":
                    break
                else:
                    print("Invalid choice.")
        
        # normal user menu
        elif choice == "4":
            user_menu(current_user)
        elif choice == "5":
            print("Goodbye.")
            return
        else:
            print("Invalid choice. Try again.")

def user_menu(current_user):
    # require login
    if not current_user:
        print("You are not logged in. Please login or register first.")
        return
    
    while True:
        # print user menu ========== 
        print(f"\nUser Menu — logged in as {current_user['username']}")
        print("1) Create task")
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
            return
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()