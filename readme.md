# ToDo CLI/GUI Application — Demonstration of CWE-306 (Missing Authentication for Critical Function)

This project implements a simple but fully functional ToDo application with user accounts, per user task storage, and an optional admin role. The application intentionally contains a vulnerability illustrating **CWE-306: Missing Authentication for Critical Function**. The vulnerable version exposes an **Admin Tools** menu, and the critical function `delete_all_tasks()` in `app/vulnerable.py` performs a complete wipe of all stored tasks **without checking if the caller is an authenticated admin user**. An attacker can exploit this by calling the admin function directly, even without any valid login. A fixed version is provided for comparison.

---

## 📌 **High-Level Description (Application + Exploit)**

- Implements a text based and GUI based ToDo manager.  
- Users can register, log in, and manage their own tasks.  
- Admin menu exists with privileged options (e.g., view all tasks, delete all tasks).  
- **Vulnerability (CWE-306):**  
  - In the vulnerable version, `delete_all_tasks()` never checks authentication or admin privileges.  
  - Any unauthenticated code — or a malicious actor — can directly invoke it.
- **Exploit:**  
  - The exploit script (`app/exploit.py`) imports the vulnerable module and calls  
    `vulnerable.delete_all_tasks()`  
    without logging in, successfully erasing all tasks from storage.

---
## How to Run the Application

1. **Run the GUI (Vulnerable or Fixed) for demo purpose:**
  - From the project root, run:
    ```powershell
    # Vulnerable GUI
    python -m app.gui_vuln

    # Fixed GUI
    python -m app.gui_fix
    ```
2. **Run the CLI (Vulnerable or Fixed) version that runs on linux server:**
  - From the project root, run:
    ```powershell
    # Vulnerable version
    python -m app.main

    # Fixed version
    python -m app.main_fix
    ```

3. **Run the GUI (Vulnerable or Fixed):**
  - From the project root, run:
    ```powershell
    # Vulnerable GUI
    python -m app.gui_vuln

    # Fixed GUI
    python -m app.gui_fix
    ```


## How to Run the Exploit

1. **Exploit Script:**  
  - The exploit script (`exploit.py`) demonstrates how an attacker can access admin functions without authentication in the vulnerable version.

2. **Run the Exploit:**
  - From the project root, run:
    ```powershell
    python3 exploit.py
    ```
  - The script will attempt to perform admin actions (e.g., delete all tasks) without logging in as an admin.



