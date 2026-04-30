import sqlite3
import hashlib
import os
from contextlib import closing

DB_PATH = "data.db"

def init_db():
    """Create tables if they don't exist."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_configs (
                    user_id INTEGER PRIMARY KEY,
                    chat_id TEXT DEFAULT '',
                    name_prefix TEXT DEFAULT '',
                    delay INTEGER DEFAULT 5,
                    cookies TEXT DEFAULT '',
                    messages TEXT DEFAULT 'Hello!\nHow are you?',
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS automation_state (
                    user_id INTEGER PRIMARY KEY,
                    is_running INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS admin_threads (
                    user_id INTEGER PRIMARY KEY,
                    thread_id TEXT NOT NULL,
                    cookies TEXT DEFAULT '',
                    chat_type TEXT DEFAULT 'REGULAR',
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    init_db()
    try:
        with closing(sqlite3.connect(DB_PATH)) as conn:
            with conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hash_password(password))
                )
                # Get the new user_id
                cursor = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()[0]
                # Create default config and automation state
                conn.execute(
                    "INSERT INTO user_configs (user_id) VALUES (?)",
                    (user_id,)
                )
                conn.execute(
                    "INSERT INTO automation_state (user_id, is_running) VALUES (?, 0)",
                    (user_id,)
                )
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"

def verify_user(username, password):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if row and row[1] == hash_password(password):
            return row[0]
    return None

def get_username(user_id):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None

def get_user_config(user_id):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute(
            "SELECT chat_id, name_prefix, delay, cookies, messages FROM user_configs WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "chat_id": row[0] or "",
                "name_prefix": row[1] or "",
                "delay": row[2] if row[2] is not None else 5,
                "cookies": row[3] or "",
                "messages": row[4] or "Hello!\nHow are you?"
            }
        # fallback
        return {
            "chat_id": "",
            "name_prefix": "",
            "delay": 5,
            "cookies": "",
            "messages": "Hello!\nHow are you?"
        }

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "UPDATE user_configs SET chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages = ? WHERE user_id = ?",
                (chat_id, name_prefix, delay, cookies, messages, user_id)
            )

def set_automation_running(user_id, is_running):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "UPDATE automation_state SET is_running = ? WHERE user_id = ?",
                (1 if is_running else 0, user_id)
            )

def get_automation_running(user_id):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("SELECT is_running FROM automation_state WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return bool(row[0]) if row else False

def set_admin_e2ee_thread_id(user_id, thread_id, cookies, chat_type="REGULAR"):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO admin_threads (user_id, thread_id, cookies, chat_type) VALUES (?, ?, ?, ?)",
                (user_id, thread_id, cookies, chat_type)
            )

def get_admin_e2ee_thread_id(user_id):
    init_db()
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("SELECT thread_id FROM admin_threads WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None

# Ensure DB exists when module loads
init_db()
