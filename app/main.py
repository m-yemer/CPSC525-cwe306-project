

from . import auth, tasks, vulnerable, storage, utils
import sys

def show_welcome():
    print("=================================================================")
    print(" ToDo CLI App — CWE-306 Demo")
    print("=================================================================")
    print()


def main_loop():
    # Ensure default users exist for demo
    auth.init_default_users()

    current_user = None

    while True:
        show_welcome()
        print("Main Menu:")
        print("1) Login")
        print("2) Register")
        print("3) Admin Tools")   # <-- intentionally shown to all 
        print("4) Use App (user features)")
        print("5) Quit")
        choice = input("> ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            password = utils.prompt_hidden("Password: ")
            user = auth.login_user(username, password)
            if not user:
                print("Login failed.")
            else:
                current_user = user
                print(f"Logged in as {current_user['username']}")
        elif choice == "2":
            username = input("Choose username: ").strip()
            password = utils.prompt_hidden("Choose password: ")
            is_admin_answer = input("Make this user admin? (y/N): ").strip().lower()
            is_admin = is_admin_answer == "y"
            user = auth.register_user(username, password, is_admin=is_admin)
            if not user:
                print("Registration failed: username probably exists.")
            else:
                print(f"Registered user {username} (admin={is_admin}). You can login now.")
        elif choice == "3":

            # The admin menu is shown & callable by anyone
            # The vulnerable functions inside do not verify authentication
            print("\n[!] Admin Tools selected (no authentication required to reach this menu)")
            vulnerable.admin_menu_interactive()
        elif choice == "4":
            user_menu(current_user)
        elif choice == "5":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

def user_menu(current_user):
    if not current_user:
        print("You are not logged in. Please login or register first.")
        return
    while True:
        print(f"\nUser Menu — logged in as {current_user['username']}")
        print("1) Create task")
        print("2) List my tasks")
        print("3) Edit my task")
        print("4) Delete my task")
        print("5) Logout")
        print("6) Back to main menu")
        choice = input("> ").strip()
        if choice == "1":
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            t = tasks.add_task(current_user['id'], title, desc)
            print(f"Created task id={t['id']}")
        elif choice == "2":
            # List my tasks 
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
                        # indent description on next line for readability
                        print(f"    desc: {desc}")
                    print(f"    created: {created}")
        elif choice == "3":
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
            done_ans = input("Mark done? (y/N): ").strip().lower()
            done = True if done_ans == "y" else False if done_ans == "n" else None
            tasks.update_task(tid, title=(new_title or None), description=(new_desc or None), done=done)
            print("Task updated.")
        elif choice == "4":
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
        elif choice == "5":
            # logout
            print(f"User {current_user['username']} logged out.")
            current_user.clear()
            return
        elif choice == "6":
            return
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_loop()
