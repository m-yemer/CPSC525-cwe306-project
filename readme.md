# CWE-306 Vulnerable Task Management Application

## High-Level Description of Exploit and Code

This project implements a multi file task management (ToDo) application designed to demonstrate **CWE-306: Missing Authentication for Critical Function**, a vulnerability that occurs when sensitive administrative functionality is accessible without proper authentication. The application includes user registration, login, task creation, updates, and deletion, as well as administrative maintenance features such as backup, restore, and mass deletion of tasks. In the **vulnerable version**, the administrative function `delete_all_tasks()` can be triggered without requiring credentials, allowing any unprivileged user to erase the entire task database. The provided `exploit.py` script invokes this vulnerable function to demonstrate how an attacker can remove all existing tasks without logging in or without giving proper admin credentials. The fixed version of the application adds strict authentication checks before accessing the admin menu and performing admin operations, preventing the exploit and closing the CWE306 vulnerability.

### Bullet Summary
- Task management system with login, registration, and administrative features  
- Explicit CWE306 vulnerability: no authentication required for `delete_all_tasks()`  
- Exploit script directly calls vulnerable function to wipe all tasks  
- Fixed version restores proper authentication and role checks  
- CLI and GUI versions included (GUI not supported on Linux servers due to use of tinkter)

---

## How to Run the Vulnerable Application
The the 4 main files is located in the **`app/.` folder** of the `CPSC525-cwe306-project/.`project folder.<br />
There are two default users:<br />
**ADMIN**`Username: alice` `Password: alicpw`<br />
**STANDARD USER** `Username: bob` `Password: bobpw`<br />

### CLI Version (Runs on Linux servers)
```bash
python3 -m app.main_vuln
```

### GUI Version (Does NOT run on Linux servers)
```bash
python3 -m app.gui_vuln
```

---

## How to Run the Fixed Application

### CLI Version (Runs on Linux servers)
```bash
python3 -m app.main_fix
```

### GUI Version (not for Linux servers)
```bash
python3 -m app.gui_fix
```

---

## How to Run the Exploit

The exploit script is located in the **root project folder**, not inside the `app/` package.

Run it with:

```bash
python3 exploit.py
```

This script triggers the vulnerable `delete_all_tasks()` admin function without authentication.

---

## Repository Contents

- `app/` — main application package  
  - `main_vuln.py` — vulnerable CLI   ;**run this for the CLI vulnerable app**
  - `main_fix.py` — fixed CLI         ;**run this for the CLI fixed app**
  - `gui_vuln.py` — vulnerable GUI    ;**run this for the GUI vulnerable app (requires Tkinter)**
  - `gui_fix.py` — fixed GUI          ;**run this for the GUI fixed app (requires Tkinter)**
  - `auth.py` — authentication logic  
  - `tasks.py` — task CRUD logic  
  - `vulnerable.py` — CWE-306 vulnerable admin actions  
  - `storage.py` — JSON-based data storage  
  - `maintenance.py` — backup/restore and data generation  
  - `utils.py` — terminal utilities  
- `exploit.py` — exploit script that deletes all tasks without authentication; ; **run this for the exploit script of the vulnerability**
- `data/` — users, tasks, audit logs  
- `readme.md` — project documentation

---

## Notes

- All CLI versions work on departmental Linux servers.  
- GUI versions only works on systems with Python Tkinter support.  
- All admin only features in the vulnerable version are intentionally left accessible to all users to demonstrate CWE-306.  

---



