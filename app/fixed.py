
from . import storage, auth
import time


def admin_menu_interactive():

    # Require admin authentication for CLI use
    username = input("Admin username: ").strip()
    password = input("Admin password: ").strip()
    admin = auth.login_user(username, password)
    if not admin:
        print("Authentication failed. Cannot access Admin Tools.")
        return
    if not admin.get("is_admin"):
        print("User is not an admin. Access denied.")
        return

    while True:
        print("\n=== ADMIN TOOLS (fixed) ===")
        print("1) Delete ALL tasks (authorized)")
        print("2) View ALL tasks")
        print("3) Back")
        choice = input("> ").strip()
        if choice == "1":
            ok = delete_all_tasks_fixed(admin)
            if ok:
                print("All tasks deleted (fixed)")
            else:
                print("Delete failed or not authorized")
        elif choice == "2":
            all_tasks = storage.load_tasks()
            if not all_tasks:
                print("(no tasks)")
            else:
                for t in all_tasks:
                    print(f"- id={t['id']} owner={t['owner_id']} title={t['title']} created={t['created_at']}")
        elif choice == "3":
            return
        else:
            print("Invalid choice")


def delete_all_tasks_fixed(admin):

    if not admin or not isinstance(admin, dict):
        return False
    if not admin.get("is_admin"):
        return False

    storage.save_tasks([])
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={admin.get('id')} time={now}")
    return True

