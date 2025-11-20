
from . import storage, auth
import time
"""
    This fixed version requires the user to be an admin before being
    able to access important admin functions.
"""

def admin_menu_interactive():

    # require admin authentification to access admin tools
    
    # admin credentials prompt
    username = input("Admin username: ").strip()
    password = input("Admin password: ").strip()

    # authenticate user
    admin = auth.login_user(username, password)
    if not admin:
        #authenticate failed by invalid user or pssword
        print("Authentication failed. Cannot access Admin Tools.")
        return
    if not admin.get("is_admin"):
        # user credntials not admin
        print("User is not an admin. Access denied.")
        return


    #Main admin menus
    while True:
        print("\n=== ADMIN TOOLS ===")
        print("1) Delete ALL tasks ")
        print("2) View ALL tasks")
        print("3) Back")
        choice = input("> ").strip() # get user chouce


        if choice == "1":
            ok = delete_all_tasks_fixed(admin) #attempt delete all
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
                    #iterate and print tasks
                    print(f"- id={t['id']} owner={t['owner_id']} title={t['title']} created={t['created_at']}")
        elif choice == "3":
            return
        else:
            print("Invalid choice")


def delete_all_tasks_fixed(admin):
    #delete all tasks present in database
    if not admin or not isinstance(admin, dict):
        return False
    if not admin.get("is_admin"):
        return False
    storage.save_tasks([])
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    storage.append_audit(f"ADMIN_DELETE_ALL performed by admin id={admin.get('id')} time={now}")
    return True

