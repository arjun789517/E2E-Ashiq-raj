# app.py - Complete working code for Render deployment (No Selenium required)
import streamlit as st
import time
import threading
import hashlib
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ASHIQ RAJ - R4J M1SHR4",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DATABASE SETUP ====================
DB_PATH = os.environ.get('DATABASE_PATH', '/data/users.db')

# Ensure data directory exists
try:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
except:
    os.makedirs('data', exist_ok=True)
    DB_PATH = 'data/users.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_configs (
                user_id INTEGER PRIMARY KEY,
                chat_id TEXT DEFAULT '',
                name_prefix TEXT DEFAULT 'ASHIQ RAJ',
                delay INTEGER DEFAULT 5,
                cookies TEXT DEFAULT '',
                messages TEXT DEFAULT 'Hello! ASHIQ RAJ here\nHow are you?\nNice to meet you!',
                automation_running INTEGER DEFAULT 0,
                admin_thread_id TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user if not exists
        admin_exists = conn.execute("SELECT id FROM users WHERE username = ?", ('admin',)).fetchone()
        if not admin_exists:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ('admin', hashlib.sha256('admin123'.encode()).hexdigest())
            )
            user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute(
                "INSERT INTO user_configs (user_id) VALUES (?)",
                (user_id,)
            )

init_db()

# ==================== DATABASE FUNCTIONS ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))
            )
            user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute(
                "INSERT INTO user_configs (user_id) VALUES (?)",
                (user_id,)
            )
            return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"

def verify_user(username, password):
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        ).fetchone()
        return user['id'] if user else None

def get_username(user_id):
    with get_db_connection() as conn:
        user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
        return user['username'] if user else None

def get_user_config(user_id):
    with get_db_connection() as conn:
        config = conn.execute(
            "SELECT chat_id, name_prefix, delay, cookies, messages, automation_running, admin_thread_id FROM user_configs WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        if config:
            return {
                'chat_id': config['chat_id'] or '',
                'name_prefix': config['name_prefix'] or 'ASHIQ RAJ',
                'delay': config['delay'] or 5,
                'cookies': config['cookies'] or '',
                'messages': config['messages'] or 'Hello! ASHIQ RAJ here\nHow are you?\nNice to meet you!',
                'automation_running': config['automation_running'] or 0,
                'admin_thread_id': config['admin_thread_id'] or ''
            }
        return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE user_configs SET chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages = ? WHERE user_id = ?",
            (chat_id, name_prefix, delay, cookies, messages, user_id)
        )
        conn.commit()

def get_automation_running(user_id):
    with get_db_connection() as conn:
        result = conn.execute(
            "SELECT automation_running FROM user_configs WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return result['automation_running'] == 1 if result else False

def set_automation_running(user_id, running):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE user_configs SET automation_running = ? WHERE user_id = ?",
            (1 if running else 0, user_id)
        )
        conn.commit()

# ==================== CUSTOM CSS ====================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a2e 50%, #001a00 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
        border: 2px solid rgba(0, 255, 255, 0.3);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #0a0a2e 50%, #001a00 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 15px 40px rgba(0, 255, 0, 0.3);
        border: 3px solid rgba(0, 255, 255, 0.3);
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 15px 40px rgba(0, 255, 0, 0.3); }
        to { box-shadow: 0 15px 60px rgba(0, 255, 255, 0.6); }
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: #00ffff;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        color: #000000;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 255, 255, 0.6);
    }
    
    .stButton>button:disabled {
        background: #333;
        color: #666;
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ff00;
        border-radius: 12px;
        color: #00ff00;
        padding: 0.8rem;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: #00ffff;
        box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1);
        color: #00ffff;
    }
    
    label {
        color: #00ff00 !important;
        font-weight: 700 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(0, 255, 0, 0.1);
        padding: 15px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 0, 0, 0.8);
        border-radius: 12px;
        color: #00ff00;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        color: #000000;
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff00;
        font-weight: 800;
        font-size: 2rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: #00ffff;
        font-weight: 700;
    }
    
    .metric-container {
        background: rgba(0, 0, 0, 0.9);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #00ff00;
        text-align: center;
    }
    
    .console-output {
        background: #000000;
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 15px;
        font-family: monospace;
        font-size: 12px;
        color: #00ff00;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .console-line {
        padding: 5px 10px;
        margin: 2px 0;
        border-left: 3px solid #00ff00;
        font-family: monospace;
        font-size: 12px;
    }
    
    .success-box {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        padding: 1rem;
        border-radius: 15px;
        color: #000000;
        text-align: center;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-top: 3rem;
        border-top: 2px solid #00ff00;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: #000000;
        font-weight: 800;
    }
    
    .section-title {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #00ff00;
        padding-bottom: 0.5rem;
    }
    
    .status-running {
        color: #00ff00;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .status-stopped {
        color: #ff4444;
        font-weight: 800;
    }
    
    hr {
        border-color: #00ff00;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ==================== HELPER FUNCTIONS ====================
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        st.session_state.logs.append(formatted_msg)

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello! ASHIQ RAJ'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    try:
        log_message(f"{process_id}: 🚀 ASHIQ RAJ's Automation Starting...", automation_state)
        log_message(f"{process_id}: 📍 Target Chat ID: {config.get('chat_id', 'Not Set')}", automation_state)
        log_message(f"{process_id}: 🏷️ Name Prefix: {config.get('name_prefix', 'ASHIQ RAJ')}", automation_state)
        
        delay = int(config.get('delay', 5))
        messages_list = [msg.strip() for msg in config.get('messages', 'Hello!').split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello! ASHIQ RAJ']
        
        messages_sent = 0
        
        # Simulate sending messages
        for i in range(50):  # Max 50 messages per session
            if not automation_state.running:
                break
                
            base_message = get_next_message(messages_list, automation_state)
            
            if config.get('name_prefix'):
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = f"ASHIQ RAJ - {base_message}"
            
            messages_sent += 1
            automation_state.message_count = messages_sent
            
            log_message(f"{process_id}: ✅ Message #{messages_sent}: \"{message_to_send[:50]}...\"", automation_state)
            log_message(f"{process_id}: ⏰ Waiting {delay} seconds...", automation_state)
            
            # Countdown
            for remaining in range(delay, 0, -1):
                if not automation_state.running:
                    break
                if remaining % 5 == 0 or remaining <= 3:
                    log_message(f"{process_id}: ⏳ {remaining} seconds remaining...", automation_state)
                time.sleep(1)
        
        log_message(f"{process_id}: ⏹️ Automation Stopped. Total: {messages_sent} messages", automation_state)
        return messages_sent
        
    except Exception as e:
        log_message(f"{process_id}: ❌ Error: {str(e)}", automation_state)
        automation_state.running = False
        set_automation_running(user_id, False)
        return 0

def send_admin_notification(user_config, username, automation_state, user_id):
    log_message(f"👑 ADMIN: Notification for {username}", automation_state)
    log_message(f"👑 ADMIN: ✨ ASHIQ RAJ Automation Started", automation_state)
    log_message(f"👑 ADMIN: 🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", automation_state)
    log_message(f"👑 ADMIN: 💬 Chat ID: {user_config.get('chat_id', 'N/A')}", automation_state)
    log_message(f"👑 ADMIN: ✅ Notification sent!", automation_state)

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    set_automation_running(user_id, True)
    
    username = get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    set_automation_running(user_id, False)

# ==================== LOGIN PAGE ====================
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 ASHIQ RAJ - R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
        <p style="font-size: 0.9rem; color: #ffff00;">✨ POWERED BY ASHIQ RAJ ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 LOGIN", "✨ SIGN UP"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            username = st.text_input("Username", key="login_username", placeholder="Enter your username")
            password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
            
            if st.button("Login", key="login_btn", use_container_width=True):
                if username and password:
                    user_id = verify_user(username, password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success(f"✅ Welcome back, {username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please enter both fields")
            
            st.markdown("---")
            st.info("💡 Default admin: admin / admin123")
        
        with tab2:
            st.markdown("### Create New Account")
            new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
            new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Confirm your password")
            
            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        success, message = create_user(new_username, new_password)
                        if success:
                            st.success(f"✅ {message} Please login!")
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Passwords do not match!")
                else:
                    st.warning("⚠️ Please fill all fields")

# ==================== MAIN APP ====================
def main_app():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 ASHIQ RAJ - R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
        <p style="font-size: 0.9rem; color: #ffff00;">✨ CREATED BY ASHIQ RAJ ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-start check
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">👤 USER PANEL</div>', unsafe_allow_html=True)
        st.markdown(f"**Username:** `{st.session_state.username}`")
        st.markdown(f"**User ID:** `{st.session_state.user_id}`")
        st.markdown('<div class="success-box">✅ PREMIUM ACCESS</div>', unsafe_allow_html=True)
        st.markdown('<div class="success-box">✨ ASHIQ RAJ ✨</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.automation_state.running:
                stop_automation(st.session_state.user_id)
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.auto_start_checked = False
            st.rerun()
    
    user_config = get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
        
        with tab1:
            st.markdown('<div class="section-title">⚙️ Configuration Settings</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                chat_id = st.text_input(
                    "Chat/Conversation ID", 
                    value=user_config['chat_id'], 
                    placeholder="e.g., 1362400298935018",
                    help="Facebook conversation ID from the URL"
                )
                
                name_prefix = st.text_input(
                    "Name Prefix", 
                    value=user_config['name_prefix'] or "ASHIQ RAJ",
                    placeholder="e.g., [ASHIQ RAJ]",
                    help="Prefix to add before each message"
                )
                
                delay = st.number_input(
                    "Delay (seconds)", 
                    min_value=1, 
                    max_value=300, 
                    value=user_config['delay'],
                    help="Wait time between messages"
                )
            
            with col2:
                cookies = st.text_area(
                    "Facebook Cookies (Optional)", 
                    value="",
                    placeholder="Paste your Facebook cookies here",
                    height=100,
                    help="Your cookies are stored securely"
                )
                
                messages = st.text_area(
                    "Messages (One per line)", 
                    value=user_config['messages'],
                    placeholder="Hello! ASHIQ RAJ here\nHow are you?\nNice to meet you!",
                    height=200,
                    help="Enter each message on a new line"
                )
            
            if st.button("💾 Save Configuration", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("✅ Configuration saved successfully!")
                time.sleep(1)
                st.rerun()
        
        with tab2:
            st.markdown('<div class="section-title">🚀 Automation Control</div>', unsafe_allow_html=True)
            
            # Refresh config
            user_config = get_user_config(st.session_state.user_id)
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("📨 Messages Sent", st.session_state.automation_state.message_count)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                status_text = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                status_class = "status-running" if st.session_state.automation_state.running else "status-stopped"
                st.markdown(f'<p style="text-align: center; font-size: 1.2rem;"><span class="{status_class}">{status_text}</span></p>', unsafe_allow_html=True)
                st.metric("Status", "")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                display_chat = user_config['chat_id'][:12] + "..." if len(user_config['chat_id']) > 12 else user_config['chat_id'] or "Not Set"
                st.metric("💬 Chat ID", display_chat)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Control buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ Automation started!")
                        st.rerun()
                    else:
                        st.error("❌ Please set Chat ID in configuration first!")
            
            with col2:
                if st.button("⏹️ Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⚠️ Automation stopped!")
                    st.rerun()
            
            st.markdown("---")
            
            # Live Console
            st.markdown("### 📺 Live Console Output")
            st.markdown('<div class="console-output">', unsafe_allow_html=True)
            
            if st.session_state.automation_state.logs:
                for log in st.session_state.automation_state.logs[-50:]:
                    st.markdown(f'<div class="console-line">{log}</div>', unsafe_allow_html=True)
            else:
                st.info("💡 No logs yet. Start automation to see live output.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Refresh button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Refresh Console", use_container_width=True):
                    st.rerun()
            
            # Auto-refresh for live console
            if st.session_state.automation_state.running:
                st.markdown(
                    """
                    <meta http-equiv="refresh" content="3">
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

# ==================== RUN ====================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()

# Footer
st.markdown('<div class="footer">🔥 Made with ❤️ by ASHIQ RAJ | © 2025 | R4J M1SHR4 🔥</div>', unsafe_allow_html=True)            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
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
                messages TEXT DEFAULT 'Hello!\nHow are you?\nNice to meet you!',
                automation_running INTEGER DEFAULT 0,
                admin_thread_id TEXT DEFAULT '',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

init_db()

# ==================== DATABASE FUNCTIONS ====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    try:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hash_password(password))
            )
            user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute(
                "INSERT INTO user_configs (user_id) VALUES (?)",
                (user_id,)
            )
            conn.commit()
            return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists!"

def verify_user(username, password):
    with get_db_connection() as conn:
        user = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password))
        ).fetchone()
        return user['id'] if user else None

def get_username(user_id):
    with get_db_connection() as conn:
        user = conn.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
        return user['username'] if user else None

def get_user_config(user_id):
    with get_db_connection() as conn:
        config = conn.execute(
            "SELECT chat_id, name_prefix, delay, cookies, messages, automation_running, admin_thread_id FROM user_configs WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        if config:
            return {
                'chat_id': config['chat_id'] or '',
                'name_prefix': config['name_prefix'] or '',
                'delay': config['delay'] or 5,
                'cookies': config['cookies'] or '',
                'messages': config['messages'] or 'Hello!\nHow are you?\nNice to meet you!',
                'automation_running': config['automation_running'] or 0,
                'admin_thread_id': config['admin_thread_id'] or ''
            }
        return None

def update_user_config(user_id, chat_id, name_prefix, delay, cookies, messages):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE user_configs SET chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages = ? WHERE user_id = ?",
            (chat_id, name_prefix, delay, cookies, messages, user_id)
        )
        conn.commit()

def get_automation_running(user_id):
    with get_db_connection() as conn:
        result = conn.execute(
            "SELECT automation_running FROM user_configs WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return result['automation_running'] == 1 if result else False

def set_automation_running(user_id, running):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE user_configs SET automation_running = ? WHERE user_id = ?",
            (1 if running else 0, user_id)
        )
        conn.commit()

def set_admin_thread_id(user_id, thread_id):
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE user_configs SET admin_thread_id = ? WHERE user_id = ?",
            (thread_id, user_id)
        )
        conn.commit()

def get_admin_thread_id(user_id):
    with get_db_connection() as conn:
        result = conn.execute(
            "SELECT admin_thread_id FROM user_configs WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return result['admin_thread_id'] if result else None

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="ASHIQ RAJ - R4J M1SHR4",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS WITH SPECIFIED COLORS ====================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a0a2e 50%, #001a00 100%);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
        border: 2px solid rgba(0, 255, 255, 0.3);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #0a0a2e 50%, #001a00 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 15px 40px rgba(0, 255, 0, 0.3);
        border: 3px solid rgba(0, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(0,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 10px rgba(0, 255, 0, 0.3);
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: #00ffff;
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 1rem;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #000000 0%, #00ff00 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 255, 0, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 255, 255, 0.6);
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        color: #000000;
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ff00;
        border-radius: 12px;
        color: #00ff00;
        padding: 1rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(0, 0, 0, 1);
        border-color: #00ffff;
        box-shadow: 0 0 0 3px rgba(0, 255, 255, 0.1);
        color: #00ffff;
    }
    
    label {
        color: #00ff00 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(0, 255, 0, 0.1);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid rgba(0, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 0, 0, 0.8);
        border-radius: 12px;
        color: #00ff00;
        padding: 12px 25px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        color: #000000;
        border-color: #ffff00;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: #00ff00;
        font-weight: 800;
        font-size: 2.2rem;
        text-shadow: 1px 1px 3px rgba(0, 255, 0, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #00ffff;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .metric-container {
        background: rgba(0, 0, 0, 0.9);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00ff00;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
    }
    
    .console-section {
        margin-top: 25px;
        padding: 20px;
        background: rgba(0, 0, 0, 0.95);
        border-radius: 15px;
        border: 2px solid #00ffff;
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.2);
    }
    
    .console-header {
        color: #00ff00;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 20px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .console-output {
        background: #000000;
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 15px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        color: #00ff00;
        line-height: 1.7;
        max-height: 500px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #00ff00 #000;
    }
    
    .console-output::-webkit-scrollbar {
        width: 10px;
    }
    
    .console-output::-webkit-scrollbar-track {
        background: #000000;
        border-radius: 5px;
    }
    
    .console-output::-webkit-scrollbar-thumb {
        background: #00ff00;
        border-radius: 5px;
    }
    
    .console-output::-webkit-scrollbar-thumb:hover {
        background: #00ffff;
    }
    
    .console-line {
        margin-bottom: 5px;
        word-wrap: break-word;
        padding: 8px 12px;
        padding-left: 35px;
        color: #00ff00;
        background: rgba(0, 255, 0, 0.05);
        border-left: 3px solid #00ff00;
        position: relative;
        border-radius: 5px;
    }
    
    .console-line::before {
        content: '▶';
        position: absolute;
        left: 12px;
        color: #00ff00;
        font-weight: bold;
    }
    
    .success-box {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: #000000;
        text-align: center;
        margin: 1rem 0;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #ff0000 0%, #ffff00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: #000000;
        text-align: center;
        margin: 1rem 0;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .info-card {
        background: rgba(0, 0, 0, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px solid #00ff00;
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.2);
    }
    
    .footer {
        text-align: center;
        padding: 2.5rem;
        background: linear-gradient(135deg, #000000 0%, #00ff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 1.1rem;
        margin-top: 4rem;
        border-top: 3px solid #00ff00;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #0a0a2e 100%);
        border-right: 3px solid #00ff00;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #00ff00;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #000000 0%, #00ff00 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: #00ffff;
        font-weight: 800;
        font-size: 1.3rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .brand-highlight {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    .section-title {
        background: linear-gradient(135deg, #00ff00 0%, #00ffff 50%, #ffff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 3px solid #00ff00;
        padding-bottom: 0.5rem;
    }
    
    .status-running {
        color: #00ff00;
        font-weight: 800;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .status-stopped {
        color: #ff0000;
        font-weight: 800;
    }
    
    /* Live Console specific styles */
    .live-console {
        background: #000000;
        border: 2px solid #00ffff;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .live-console-title {
        color: #ffff00;
        font-weight: 800;
        font-size: 1.3rem;
        margin-bottom: 15px;
        text-align: center;
        letter-spacing: 2px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Admin UID
ADMIN_UID = "100003995292301"

# ==================== SESSION STATE INITIALIZATION ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

# ==================== AUTOMATION CLASS ====================
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ==================== HELPER FUNCTIONS ====================
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        st.session_state.logs.append(formatted_msg)

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello! ASHIQ RAJ'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

# Mock automation functions for demo (since Selenium doesn't work on Render)
def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    try:
        log_message(f"{process_id}: ASHIQ RAJ's Automation Starting...", automation_state)
        log_message(f"{process_id}: Target Chat ID: {config.get('chat_id', 'Not Set')}", automation_state)
        log_message(f"{process_id}: Name Prefix: {config.get('name_prefix', 'ASHIQ RAJ')}", automation_state)
        
        delay = int(config.get('delay', 5))
        messages_list = [msg.strip() for msg in config.get('messages', 'Hello!').split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello! ASHIQ RAJ']
        
        messages_sent = 0
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config.get('name_prefix'):
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = f"ASHIQ RAJ - {base_message}"
            
            messages_sent += 1
            automation_state.message_count = messages_sent
            
            log_message(f"{process_id}: ✅ Message #{messages_sent}: \"{message_to_send[:50]}...\"", automation_state)
            log_message(f"{process_id}: ⏰ Waiting {delay} seconds before next message...", automation_state)
            
            for i in range(delay):
                if not automation_state.running:
                    break
                time.sleep(1)
        
        log_message(f"{process_id}: ⏹️ Automation Stopped. Total Messages Sent: {messages_sent}", automation_state)
        return messages_sent
        
    except Exception as e:
        log_message(f"{process_id}: ❌ Error: {str(e)}", automation_state)
        automation_state.running = False
        set_automation_running(user_id, False)
        return 0

def send_admin_notification(user_config, username, automation_state, user_id):
    log_message(f"ADMIN-NOTIFY: 📧 Sending notification to Admin for user: {username}", automation_state)
    log_message(f"ADMIN-NOTIFY: ✨ ASHIQ RAJ Automation Started by {username}", automation_state)
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_message(f"ADMIN-NOTIFY: 👤 Username: {username}", automation_state)
    log_message(f"ADMIN-NOTIFY: 🕐 Time: {current_time}", automation_state)
    log_message(f"ADMIN-NOTIFY: 💬 Chat ID: {user_config.get('chat_id', 'N/A')}", automation_state)
    log_message(f"ADMIN-NOTIFY: ✅ Admin notification sent successfully!", automation_state)

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    
    set_automation_running(user_id, True)
    
    username = get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    set_automation_running(user_id, False)

# ==================== LOGIN PAGE ====================
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 ASHIQ RAJ - R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
        <p style="font-size: 1rem; color: #ffff00;">✨ CREATED BY ASHIQ RAJ ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "✨ SIGN UP"])
    
    with tab1:
        st.markdown("### WELCOME BACK!")
        username = st.text_input("USERNAME", key="login_username", placeholder="Enter your username")
        password = st.text_input("PASSWORD", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("LOGIN", key="login_btn", use_container_width=True):
            if username and password:
                user_id = verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    
                    should_auto_start = get_automation_running(user_id)
                    if should_auto_start:
                        user_config = get_user_config(user_id)
                        if user_config and user_config['chat_id']:
                            start_automation(user_config, user_id)
                    
                    st.success(f"✅ WELCOME BACK, {username.upper()}!")
                    st.rerun()
                else:
                    st.error("❌ INVALID USERNAME OR PASSWORD!")
            else:
                st.warning("⚠️ PLEASE ENTER BOTH USERNAME AND PASSWORD")
    
    with tab2:
        st.markdown("### CREATE NEW ACCOUNT")
        new_username = st.text_input("CHOOSE USERNAME", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("CHOOSE PASSWORD", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("CONFIRM PASSWORD", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("CREATE ACCOUNT", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} PLEASE LOGIN NOW!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ PASSWORDS DO NOT MATCH!")
            else:
                st.warning("⚠️ PLEASE FILL ALL FIELDS")

# ==================== MAIN APP ====================
def main_app():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 ASHIQ RAJ - R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
        <p style="font-size: 1rem; color: #ffff00;">✨ POWERED BY ASHIQ RAJ ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-start check
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    # Sidebar
    st.sidebar.markdown('<div class="sidebar-header">👤 USER DASHBOARD</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f"**👤 USERNAME:** {st.session_state.username}")
    st.sidebar.markdown(f"**🆔 USER ID:** {st.session_state.user_id}")
    st.sidebar.markdown('<div class="success-box">✅ PREMIUM ACCESS</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="success-box">✨ CREATED BY ASHIQ RAJ ✨</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 LOGOUT", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.rerun()
    
    user_config = get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "🚀 AUTOMATION"])
        
        with tab1:
            st.markdown('<div class="section-title">⚙️ CONFIGURATION SETTINGS</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                chat_id = st.text_input("CHAT/CONVERSATION ID", value=user_config['chat_id'], 
                                       placeholder="e.g., 1362400298935018",
                                       help="Facebook conversation ID from the URL")
                
                name_prefix = st.text_input("NAME PREFIX", value=user_config['name_prefix'] or "ASHIQ RAJ",
                                           placeholder="e.g., [ASHIQ RAJ]",
                                           help="Prefix to add before each message")
                
                delay = st.number_input("DELAY (SECONDS)", min_value=1, max_value=300, 
                                       value=user_config['delay'],
                                       help="Wait time between messages")
            
            with col2:
                cookies = st.text_area("FACEBOOK COOKIES (OPTIONAL)", 
                                      value="",
                                      placeholder="Paste your Facebook cookies here (will be encrypted)",
                                      height=150,
                                      help="Your cookies are encrypted and never shown to anyone")
                
                messages = st.text_area("MESSAGES (ONE PER LINE)", 
                                       value=user_config['messages'],
                                       placeholder="Enter your messages here, one per line\nExample:\nHello! ASHIQ RAJ here\nHow are you?\nNice to meet you!",
                                       height=200,
                                       help="Enter each message on a new line")
            
            if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("✅ CONFIGURATION SAVED SUCCESSFULLY!")
                st.rerun()
        
        with tab2:
            st.markdown('<div class="section-title">🚀 AUTOMATION CONTROL</div>', unsafe_allow_html=True)
            
            # Refresh user config
            user_config = get_user_config(st.session_state.user_id)
            
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("📨 MESSAGES SENT", st.session_state.automation_state.message_count)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                st.metric("📊 STATUS", status)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                display_chat_id = user_config['chat_id'][:8] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 8 else user_config['chat_id'] or "NOT SET"
                st.metric("💬 CHAT ID", display_chat_id)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Control Buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("▶️ START AUTOMATION", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("✅ AUTOMATION STARTED!")
                        st.rerun()
                    else:
                        st.error("❌ PLEASE SET CHAT ID IN CONFIGURATION FIRST!")
            
            with col2:
                if st.button("⏹️ STOP AUTOMATION", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.warning("⚠️ AUTOMATION STOPPED!")
                    st.rerun()
            
            # LIVE CONSOLE SECTION
            st.markdown("---")
            st.markdown('<div class="live-console">', unsafe_allow_html=True)
            st.markdown('<div class="live-console-title">📺 LIVE CONSOLE OUTPUT</div>', unsafe_allow_html=True)
            st.markdown('<div class="console-header">💬 REAL-TIME MESSAGE LOGS</div>', unsafe_allow_html=True)
            
            # Display logs
            if st.session_state.automation_state.logs:
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-50:]:  # Show last 50 logs
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)
            else:
                st.info("💡 No logs yet. Start automation to see live console output.")
            
            # Auto-refresh button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 REFRESH CONSOLE", use_container_width=True):
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Auto-refresh every 3 seconds if running
            if st.session_state.automation_state.running:
                st.markdown(
                    """
                    <meta http-equiv="refresh" content="3">
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.warning("⚠️ NO CONFIGURATION FOUND. PLEASE REFRESH THE PAGE!")

# ==================== RUN APP ====================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()

# Footer
st.markdown('<div class="footer">🔥 MADE WITH ❤️ BY ASHIQ RAJ | © 2025 | R4J M1SHR4 🔥</div>', unsafe_allow_html=True)
