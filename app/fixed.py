
from . import storage, auth
from .session import AuthenticatedAdminSession
import time
"""
    This fixed version requires the user to be an admin before being
    able to access important admin functions.
"""

def admin_menu_interactive():
    # require admin authentification to access admin tools
    username = input("Admin username: ").strip()
    password = input("Admin password: ").strip()

    # authenticate user and require admin session
    admin_session = auth.login_user(username, password, require_admin_session=True)
    if not admin_session or not isinstance(admin_session, AuthenticatedAdminSession) or not admin_session.is_valid():
        print("Authentication failed or not authorized. Cannot access Admin Tools.")
        return

    #Main admin menus
    while True:
        print("\n=== ADMIN TOOLS ===")
        print("1) Delete ALL tasks ")
        print("2) View ALL tasks")
        print("3) Back")
        choice = input("> ").strip() # get user choice

        if choice == "1":
            ok = delete_all_tasks_fixed(admin_session) #attempt delete all
            if ok:
                print("All tasks deleted")
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


def delete_all_tasks_fixed(admin_session):
    # Only allow if admin_session is a real AuthenticatedAdminSession
    if not admin_session or not isinstance(admin_session, AuthenticatedAdminSession):
        return False
    if not admin_session.is_valid():
        return False
    storage.save_tasks([])
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={admin_session.id} time={now}")
    return True

