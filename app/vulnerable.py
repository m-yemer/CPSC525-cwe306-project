


from . import storage, tasks
import time

def admin_menu_interactive():
    # vulnerable admin menu access without authentification

    while True:
        print("\n=== ADMIN TOOLS ===")
        print("1) Delete ALL tasks (vulnerable)") #no authentification check
        print("2) View ALL tasks") # see users tasks
        print("3) Back")
        choice = input("> ").strip()
        if choice == "1":
            delete_all_tasks()   # call the vulnerable delete all tasks function
        elif choice == "2":
            all_tasks = storage.load_tasks() # load all tasks
            if not all_tasks:
                print("(no tasks)")
            else:
                for t in all_tasks:
                    print(f"- id={t['id']} owner={t['owner_id']} title={t['title']} created={t['created_at']}")
        elif choice == "3": # exit menu
            return
        else:
            print("Invalid choice")

def delete_all_tasks():
    #vulnerable function to delete tasks database
    #no admin authentification check, so any user can acces and delete all 

    storage.save_tasks([])  
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    storage.append_audit(f"ADMIN_DELETE_ALL invoked (unauthenticated) time={now}")





