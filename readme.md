# ToDo CLI App — CWE-306 Vulnerability

This is a deliberately ToDo application created to demonstrate
CWE-306: Missing Authentication for Critical Function.

## What it does
- Users can register and log in.
- Users can create/list/edit/delete their own tasks.
- The app includes an **Admin Tools** menu and an admin operation that *deletes all tasks*.
- **Vulnerability:** The admin functionality is exposed and the critical function `delete_all_tasks()` 
  in `app/vulnerable.py` performs the deletion without verifying whether the caller is authenticated or is an admin.


## Quick start
1. Run the app from powershell:
  -python -m app.gui_vuln
  -python -m app.gui_fix
