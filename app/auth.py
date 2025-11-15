
# User registration, login, and simple password hashing
# Uses storage.py to persist users

import hashlib
import time
from typing import Optional, Dict
from . import storage


SALT = b"cpsc525_demo_salt"

def _hash_password(password: str) -> str:
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
                "is_admin": True,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
        if "bob" not in names:
            users.append({
                "id": storage.next_id(users),
                "username": "bob",
                "password_hash": _hash_password("bobpw"),
                "is_admin": False,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            })
        storage.save_users(users)

def find_user_by_username(username: str) -> Optional[Dict]:
    users = storage.load_users()
    for u in users:
        if u.get("username") == username:
            return u
    return None

def register_user(username: str, password: str, is_admin: bool=False) -> Optional[Dict]:
    users = storage.load_users()
    if any(u["username"] == username for u in users):
        return None
    uid = storage.next_id(users)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    user = {
        "id": uid,
        "username": username,
        "password_hash": _hash_password(password),
        "is_admin": is_admin,
        "created_at": now
    }
    users.append(user)
    storage.save_users(users)
    storage.append_audit(f"REGISTER: {username} id={uid} time={now}")
    return user

def verify_password(user: Dict, password: str) -> bool:
    return user.get("password_hash") == _hash_password(password)

def login_user(username: str, password: str) -> Optional[Dict]:
    user = find_user_by_username(username)
    if not user:
        return None
    if not verify_password(user, password):
        return None
    storage.append_audit(f"LOGIN: {username} id={user['id']}")
    return user
