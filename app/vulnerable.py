


from . import storage, tasks
import time

def admin_menu_interactive():

    while True:
        print("\n=== ADMIN TOOLS ===")
        print("1) Delete ALL tasks (vulnerable)")
        print("2) View ALL tasks")
        print("3) Back")
        choice = input("> ").strip()
        if choice == "1":
            delete_all_tasks()  
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

def delete_all_tasks():


    storage.save_tasks([])  
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    storage.append_audit(f"ADMIN_DELETE_ALL invoked (unauthenticated) time={now}")





