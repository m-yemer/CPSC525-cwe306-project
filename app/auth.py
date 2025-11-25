

import hashlib
import time
from typing import Optional, Dict, Union
from .session import AuthenticatedAdminSession
from . import storage

#password salt for hash
SALT = b"cpsc525_cwe306"

def _hash_password(password: str) -> str:
    #simple password hash
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), SALT, 100_000)
    return h.hex()

def init_default_users():
    """
    Ensure that default users exist
    username / password:
    alice / alicepw (admin)
    bob   / bobpw   (normal user)
    """
    users = storage.load_users()
    # If no users file or empty, make sample users
    if not users:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        users = [
            {
                "id": 1,
                "username": "alice",
                "password_hash": _hash_password("alicepw"),
                "is_admin": True,
                "created_at": now
            },
            {
                "id": 2,
                "username": "bob",
                "password_hash": _hash_password("bobpw"),
                "is_admin": False,
                "created_at": now
            }
        ]
        storage.save_users(users)
    else:
        # ensure passwords are present for at least alice/bob if they exist
        names = {u["username"]: u for u in users}
        if "alice" not in names:
            users.append({
                "id": storage.next_id(users),
                "username": "alice",
                "password_hash": _hash_password("alicepw"),
                "is_admin": True, # alice is set to admin
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
        if "bob" not in names:
            users.append({
                "id": storage.next_id(users),
                "username": "bob",
                "password_hash": _hash_password("bobpw"),
                "is_admin": False, # bob set to general user
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
        storage.save_users(users)

def find_user_by_username(username: str) -> Optional[Dict]:
    #look up username in dicitionary, if found return user else none
    users = storage.load_users()
    for u in users:
        if u.get("username") == username: # find match
            return u
    return None

def register_user(username: str, password: str, is_admin: bool=False) -> Optional[Dict]:
    # register a new user with given username and password
    users = storage.load_users()
    if any(u["username"] == username for u in users): # check if username already exists
        return None
    uid = storage.next_id(users) # unique user id
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) # creation time stamp for log
    user = {
        "id": uid,
        "username": username,
        "password_hash": _hash_password(password),
        "is_admin": is_admin,
        "created_at": now
    }
    users.append(user) # add user to list
    storage.save_users(users) # persistant storage
    storage.append_audit(f"REGISTER: {username} id={uid} time={now}") # log register
    return user

def verify_password(user: Dict, password: str) -> bool:
    # for login verify password provided matches hash stored
    return user.get("password_hash") == _hash_password(password)

def login_user(username: str, password: str, require_admin_session: bool = False) -> Union[Dict, AuthenticatedAdminSession, None]:
    # authenticate username and password in login
    user = find_user_by_username(username)
    if not user: # no username exists
        return None
    if not verify_password(user, password): # check password
        return None
    storage.append_audit(f"LOGIN: {username} id={user['id']}") # log sucess
    if require_admin_session and user.get("is_admin"):
        return AuthenticatedAdminSession(user)
    return user # return authenticated user
