

from typing import List, Dict, Any, Optional
from . import storage
import time

def list_all_tasks() -> List[Dict]:
    # return listt of all tasks in storage
    return storage.load_tasks()

def list_tasks_for_user(user_id: int) -> List[Dict]:
    # retun list of tasks owned by specific user
    tasks = storage.load_tasks()
    return [t for t in tasks if t.get("owner_id") == user_id]

def add_task(owner_id: int, title: str, description: str="") -> Dict:
    # create new task for user and save
    #requies param: owner_id for id of owner user, title for name of task
    # and description to describe task but it is optional to add
    tasks = storage.load_tasks()
    tid = storage.next_id(tasks) # generate task id
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) # time stamp
    task = {
        "id": tid,
        "owner_id": owner_id,
        "title": title,
        "description": description,
        "done": False,
        "created_at": now
    }
    tasks.append(task)
    storage.save_tasks(tasks)
    storage.append_audit(f"TASK_CREATE: user={owner_id} task={tid} title={title}")
    return task

def get_task(task_id: int) -> Optional[Dict]:
    # retrieve task by ID, return none if doesnt exist
    tasks = storage.load_tasks()
    for t in tasks:
        if t.get("id") == task_id:
            return t
    return None

def update_task(task_id: int, title: str=None, description: str=None, done: bool=None) -> bool:
    # update any of the fields of title, description and completion (done)
    tasks = storage.load_tasks()
    for t in tasks:
        if t.get("id") == task_id:
            if title is not None:
                t["title"] = title
            if description is not None:
                t["description"] = description
            if done is not None:
                t["done"] = bool(done)
            storage.save_tasks(tasks)
            storage.append_audit(f"TASK_UPDATE: task={task_id}")
            return True
    return False

def delete_task(task_id: int) -> bool:
    # delete task by its id
    tasks = storage.load_tasks()
    new_tasks = [t for t in tasks if t.get("id") != task_id]
    if len(new_tasks) == len(tasks):
        return False
    storage.save_tasks(new_tasks)
    storage.append_audit(f"TASK_DELETE: task={task_id}")
    return True
