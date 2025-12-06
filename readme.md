# CWE-306 Vulnerable Task Management Application

## High-Level Description of CWE-306 Exploit and the Application Code

This project implements a multi file task management (ToDo) application designed to demonstrate **CWE-306: Missing Authentication for Critical Function**, a vulnerability that occurs when sensitive administrative functionality is accessible without proper authentication. The application includes user registration, login, task creation, updates, and deletion, as well as administrative maintenance features such as backup, restore, and mass deletion of tasks. In the **vulnerable version**, the administrative function `delete_all_tasks()` in `vulnerable.py` can be triggered without requiring credentials, allowing any unprivileged user to erase the entire task database. The provided `exploit.py` script invokes this vulnerable function to demonstrate how an attacker can remove all existing tasks without logging in or without giving proper admin credentials. The fixed version of the application adds strict authentication checks before accessing the admin menu and performing admin operations, preventing the exploit and closing the CWE306 vulnerability.

### How the Fixed Code Works

The fixed version (`fixed.py`) eliminates the present CWE-306 vulnerability by requiring authentication at the admin menu and within critical functions. The `admin_menu_interactive()` function now prompts for admin credentials before granting access, and the `delete_all_tasks_fixed()` function validates an `AuthenticatedAdminSession` object through type checking and session validity verification. This multi check approach ensures that only properly authenticated administrators can access and execute sensitive operations. The vulnerable version's `delete_all_tasks()` had no such protections and could be called directly from anywhere without any credentials, as demonstrated by the exploit script.

### Bullet Summary
- Task management system with login, registration, and administrative features  
- Explicit CWE306 vulnerability: no authentication required for `delete_all_tasks()`  
- Exploit script directly calls vulnerable function to wipe all tasks  
- Fixed version requires admin credentials at menu entry and validates `AuthenticatedAdminSession` in critical functions 
- CLI and GUI versions included

---
# Running the GUI Remotely with SSH (X11 Forwarding)

To run the GUI of this project from the university’s remote server on your own computer, we use **X11 forwarding**. This lets programs running on the server open windows directly on your local machine.

## 1. Install an X11 Server (Windows)

You need to install an X11 server:

* **VcXsrv**: [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)

After installing, start VcXsrv (the default **Multiple windows** is what we used).

## 2. Set Your DISPLAY Variable

 In PowerShell/Terminal, run:

```powershell
setx DISPLAY localhost:0.0
```
To display GUI on machine.

## 3. SSH Into the Remote Server (with X11 Forwarding)

Use SSH with the `-Y` option to turn on trusted X11 forwarding. Replace `<your-username>` with your actual UC username:

```bash
ssh -Y <your-username>@csx1.ucalgary.ca
```

Once connected, any GUI program you run on the server should show up on your computer through VcXsrv.

---


---
# Info on How to Run the Applications
The the 4 main files is located in the **`app/.` folder** of the `CPSC525-cwe306-project/.`  
There are two default users present in the project given that have admin privilege and standard user privilege. 

**ADMIN**`Username: alice` `Password: alicepw` 

**STANDARD USER** `Username: bob` `Password: bobpw`  

All of the following commands to run should be done in the root `CPSC525-cwe306-project/.` folder. 

### Go to Project Directory 
```bash
cd CPSC525-cwe306-project
```

---
## How to Run the Vulnerable Application

### CLI Version 
```bash
python3 -m app.main_vuln
```

### GUI Version 
```bash
python3 -m app.gui_vuln
```

---

## How to Run the Fixed Application

### CLI Version 
```bash
python3 -m app.main_fix
```

### GUI Version 
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
- `exploit_fix.py` - mainly just a sanity check to make sure the fixed function actually works 
- `exploit.py` — exploit script that deletes all tasks without authentication; ; **run this for the exploit script of the vulnerability**
- `test_cli_menus.py` — test script for CLI menu functionality
- `data/` — users, tasks, audit logs  
- `readme.md` — project documentation 



---


---



