from pathlib import Path
import json
import shutil
import time
from typing import Optional

from . import storage, auth, tasks

DATA_DIR = Path(storage.DATA_DIR)
BACKUP_DIR = DATA_DIR / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def backup_data() -> Path:

    ts = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    target = BACKUP_DIR / f"backup_{ts}"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("users.json", "tasks.json", "audit.log"):
        src = DATA_DIR / name
        if src.exists():
            shutil.copy2(src, target / name)
    return target

def restore_backup(backup_path: str) -> bool:

    src = Path(backup_path)
    if not src.is_dir():
        src = BACKUP_DIR / backup_path
    if not src.is_dir():
        return False
    for f in ("users.json", "tasks.json", "audit.log"):
        s = src / f
        if s.exists():
            shutil.copy2(s, DATA_DIR / f)
    return True

def stats() -> dict:
    # show the basic info on the data base to admin
    users = storage.load_users() or []
    tasks_list = storage.load_tasks() or []
    by_user = {}
    for t in tasks_list:
        owner = t.get("owner_id")
        by_user.setdefault(owner, 0)
        by_user[owner] += 1
    return {
        "users": len(users),
        "tasks": len(tasks_list),
        "tasks_per_user_sample": dict(list(by_user.items())[:10])
    }

def generate_sample_data(add_users: int = 10, tasks_per_user: int = 10, password: str = "pw"):
    # generate sample data (users and tasks) mainly just for demo purposes
    auth.init_default_users()
    base = storage.load_users() or []
    start = max((u.get("id", 0) for u in base), default=0) + 1
    created = []
    for i in range(add_users):
        uname = f"gen_{int(time.time())}_{i}"
        user = auth.register_user(uname, password, is_admin=False)
        if user:
            created.append(user)
    # create tasks
    for u in created:
        for j in range(tasks_per_user):
            tasks.add_task(u["id"], f"sample task {j} for {u['username']}", "auto-generated")
    return {"created_users": len(created), "created_tasks": len(created) * tasks_per_user}

def menu(current_user: Optional[dict]):

    while True:
        print("\n=== MAINTENANCE ===")
        print("1) Show stats")
        print("2) Backup data (admin)")
        print("3) Restore from backup (admin)")
        print("4) Generate sample data")
        print("5) Back")
        choice = input("> ").strip()
        if choice == "1":
            s = stats()
            print(json.dumps(s, indent=2))
        elif choice == "2":
            if not current_user or not current_user.get("is_admin"):
                print("Admin required.")
                continue
            p = backup_data()
            print(f"Backup created: {p}")
        elif choice == "3":
            if not current_user or not current_user.get("is_admin"):
                print("Admin required.")
                continue
            name = input("Backup name or dir: ").strip()
            ok = restore_backup(name)
            print("Restore succeeded." if ok else "Restore failed.")
        elif choice == "4":
            u = input("Additional users to create (default 10): ").strip()
            t = input("Tasks per user (default 10): ").strip()
            try:
                nu = int(u) if u else 10
                nt = int(t) if t else 10
            except ValueError:
                print("Invalid numbers.")
                continue
            res = generate_sample_data(nu, nt)
            print(f"Generated {res['created_users']} users and {res['created_tasks']} tasks.")
        elif choice == "5":
            return
        else:
            print("Invalid choice.")