# json storage management for users and tasks

import json
import os
import time
from typing import List, Dict, Any

# define paths for data direcgtory and respective json files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
AUDIT_FILE = os.path.join(DATA_DIR, "audit.log")

def ensure_data_dir():
    # make data directory if doesnt exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def read_json_file(path: str) -> List[Dict[str, Any]]:
    #read the json and return directories list
    ensure_data_dir() #
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def write_json_file(path: str, data):
    # write data to the json file
    ensure_data_dir()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_users() -> List[Dict]:
    #load all user from users.json
    users = read_json_file(USERS_FILE)
    if not users:
        # create a default admin user and a normal user 
        
        default_admin = {
            "id": 1,
            "username": "alice",
            "password_hash": "",  # fill after auth module import
            "is_admin": True,
            "created_at": None
        }
        default_user = {
            "id": 2,
            "username": "bob",
            "password_hash": "",
            "is_admin": False,
            "created_at": None
        }
        
        return []
    return users

def save_users(users: List[Dict]):
    # save list of user to users.json
    write_json_file(USERS_FILE, users)

def load_tasks() -> List[Dict]:
    # load all tasks from tasks.json
    tasks = read_json_file(TASKS_FILE)
    return tasks

def save_tasks(tasks: List[Dict]):
    # save all tasks to tasks.json
    write_json_file(TASKS_FILE, tasks)

def append_audit(entry: str):
    # append log entry with utc time
    ensure_data_dir()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) 
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{entry} time={now} UTC\n")

def next_id(items: List[Dict]) -> int:
    # return the nect int id for a list of items
    # find max current id and adds 1 or return 1 if empty
    if not items:
        return 1
    return max(item.get("id", 0) for item in items) + 1
