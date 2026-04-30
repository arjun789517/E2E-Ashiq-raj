import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="R4J M1SHR4",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #ffe6f2 50%, #ffccff 100%);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(255, 105, 180, 0.2);
        border: 2px solid rgba(255, 182, 193, 0.3);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .main-header {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 50%, #dc143c 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 15px 40px rgba(255, 20, 147, 0.3);
        border: 3px solid rgba(255, 255, 255, 0.3);
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
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 1rem;
        text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.4);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 20, 147, 0.6);
        background: linear-gradient(135deg, #ff1493 0%, #dc143c 100%);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid #ffb6c1;
        border-radius: 12px;
        color: #333;
        padding: 1rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 1);
        border-color: #ff1493;
        box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.1);
        color: #333;
    }
    
    label {
        color: #ff1493 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 182, 193, 0.2);
        padding: 15px;
        border-radius: 15px;
        border: 2px solid rgba(255, 105, 180, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 12px;
        color: #ff1493;
        padding: 12px 25px;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
        color: white;
        border-color: #ff1493;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: #ff1493;
        font-weight: 800;
        font-size: 2.2rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stMetricLabel"] {
        color: #ff6b9d;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ffb6c1;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.1);
    }
    
    .console-section {
        margin-top: 25px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        border: 2px solid #ff1493;
        box-shadow: 0 4px 20px rgba(255, 20, 147, 0.1);
    }
    
    .console-header {
        color: #ff1493;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 20px;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .console-output {
        background: #1a1a1a;
        border: 2px solid #ff1493;
        border-radius: 12px;
        padding: 15px;
        font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        color: #00ff88;
        line-height: 1.7;
        max-height: 500px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #ff1493 #333;
    }
    
    .console-output::-webkit-scrollbar {
        width: 10px;
    }
    
    .console-output::-webkit-scrollbar-track {
        background: #333;
        border-radius: 5px;
    }
    
    .console-output::-webkit-scrollbar-thumb {
        background: #ff1493;
        border-radius: 5px;
    }
    
    .console-output::-webkit-scrollbar-thumb:hover {
        background: #ff6b9d;
    }
    
    .console-line {
        margin-bottom: 5px;
        word-wrap: break-word;
        padding: 8px 12px;
        padding-left: 35px;
        color: #00ff88;
        background: rgba(255, 20, 147, 0.05);
        border-left: 3px solid #ff1493;
        position: relative;
        border-radius: 5px;
    }
    
    .console-line::before {
        content: '►';
        position: absolute;
        left: 12px;
        color: #ff1493;
        font-weight: bold;
    }
    
    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        font-weight: 700;
        font-size: 1.1rem;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 2px solid #ffb6c1;
        box-shadow: 0 8px 25px rgba(255, 105, 180, 0.15);
    }
    
    .footer {
        text-align: center;
        padding: 2.5rem;
        color: #ff1493;
        font-weight: 800;
        font-size: 1.1rem;
        margin-top: 4rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        border-top: 3px solid #ff1493;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #ffe6f2 100%);
        border-right: 3px solid #ff1493;
    }
    
    [data-testid="stSidebar"] .element-container {
        color: #ff1493;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
        padding: 2rem 1rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        font-weight: 800;
        font-size: 1.3rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .brand-highlight {
        background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    .section-title {
        color: #ff1493;
        font-weight: 800;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 3px solid #ffb6c1;
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
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_UID = "100003995292301"

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

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                        
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}: ✅ Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}: ✅ Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}: ✅ Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue
    
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass
    
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id, automation_state)
        
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}: ✅ Sent via Enter: "{message_to_send[:30]}..."', automation_state)
                else:
                    log_message(f'{process_id}: ✅ Sent via button: "{message_to_send[:30]}..."', automation_state)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state)
                time.sleep(5)
        
        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state)
        return messages_sent
        
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        log_message(f"ADMIN-NOTIFY: Preparing admin notification...", automation_state)
        
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
        
        if admin_e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Using saved admin thread: {admin_e2ee_thread_id}", automation_state)
        
        driver = setup_browser(automation_state)
        
        log_message(f"ADMIN-NOTIFY: Navigating to Facebook...", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if user_config['cookies'] and user_config['cookies'].strip():
            log_message(f"ADMIN-NOTIFY: Adding cookies...", automation_state)
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        user_chat_id = user_config.get('chat_id', '')
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
        chat_type = 'REGULAR'
        
        if e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Opening saved admin conversation...", automation_state)
            
            if '/e2ee/' in str(e2ee_thread_id) or admin_e2ee_thread_id:
                conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}'
                chat_type = 'E2EE'
            else:
                conversation_url = f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
                chat_type = 'REGULAR'
            
            log_message(f"ADMIN-NOTIFY: Opening {chat_type} conversation: {conversation_url}", automation_state)
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
        
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Searching for admin UID: {ADMIN_UID}...", automation_state)
            
            try:
                profile_url = f'https://www.facebook.com/{ADMIN_UID}'
                log_message(f"ADMIN-NOTIFY: Opening admin profile: {profile_url}", automation_state)
                driver.get(profile_url)
                time.sleep(8)
                
                message_button_selectors = [
                    'div[aria-label*="Message" i]',
                    'a[aria-label*="Message" i]',
                    'div[role="button"]:has-text("Message")',
                    'a[role="button"]:has-text("Message")',
                    '[data-testid*="message"]'
                ]
                
                message_button = None
                for selector in message_button_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for elem in elements:
                                text = elem.text.lower() if elem.text else ""
                                aria_label = elem.get_attribute('aria-label') or ""
                                if 'message' in text or 'message' in aria_label.lower():
                                    message_button = elem
                                    log_message(f"ADMIN-NOTIFY: Found message button: {selector}", automation_state)
                                    break
                            if message_button:
                                break
                    except:
                        continue
                
                if message_button:
                    log_message(f"ADMIN-NOTIFY: Clicking message button...", automation_state)
                    driver.execute_script("arguments[0].click();", message_button)
                    time.sleep(8)
                    
                    current_url = driver.current_url
                    log_message(f"ADMIN-NOTIFY: Redirected to: {current_url}", automation_state)
                    
                    if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                        if '/e2ee/t/' in current_url:
                            e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'E2EE'
                            log_message(f"ADMIN-NOTIFY: ✅ Found E2EE conversation: {e2ee_thread_id}", automation_state)
                        else:
                            e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'REGULAR'
                            log_message(f"ADMIN-NOTIFY: ✅ Found REGULAR conversation: {e2ee_thread_id}", automation_state)
                        
                        if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                            current_cookies = user_config.get('cookies', '')
                            db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                            admin_found = True
                    else:
                        log_message(f"ADMIN-NOTIFY: Message button didn't redirect to messages page", automation_state)
                else:
                    log_message(f"ADMIN-NOTIFY: Could not find message button on profile", automation_state)
            
            except Exception as e:
                log_message(f"ADMIN-NOTIFY: Profile approach failed: {str(e)[:100]}", automation_state)
            
            if not admin_found or not e2ee_thread_id:
                log_message(f"ADMIN-NOTIFY: ⚠️ Could not find admin via search, trying DIRECT MESSAGE approach...", automation_state)
                
                try:
                    profile_url = f'https://www.facebook.com/messages/new'
                    log_message(f"ADMIN-NOTIFY: Opening new message page...", automation_state)
                    driver.get(profile_url)
                    time.sleep(8)
                    
                    search_box = None
                    search_selectors = [
                        'input[aria-label*="To:" i]',
                        'input[placeholder*="Type a name" i]',
                        'input[type="text"]'
                    ]
                    
                    for selector in search_selectors:
                        try:
                            search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if search_elements:
                                for elem in search_elements:
                                    if elem.is_displayed():
                                        search_box = elem
                                        log_message(f"ADMIN-NOTIFY: Found 'To:' box with: {selector}", automation_state)
                                        break
                                if search_box:
                                    break
                        except:
                            continue
                    
                    if search_box:
                        log_message(f"ADMIN-NOTIFY: Typing admin UID in new message...", automation_state)
                        driver.execute_script("""
                            arguments[0].focus();
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        """, search_box, ADMIN_UID)
                        time.sleep(5)
                        
                        result_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="option"], li[role="option"], a[role="option"]')
                        if result_elements:
                            log_message(f"ADMIN-NOTIFY: Found {len(result_elements)} results, clicking first...", automation_state)
                            driver.execute_script("arguments[0].click();", result_elements[0])
                            time.sleep(8)
                            
                            current_url = driver.current_url
                            if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                                if '/e2ee/t/' in current_url:
                                    e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'E2EE'
                                    log_message(f"ADMIN-NOTIFY: ✅ Direct message opened E2EE: {e2ee_thread_id}", automation_state)
                                else:
                                    e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'REGULAR'
                                    log_message(f"ADMIN-NOTIFY: ✅ Direct message opened REGULAR chat: {e2ee_thread_id}", automation_state)
                                
                                if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                                    admin_found = True
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Direct message approach failed: {str(e)[:100]}", automation_state)
        
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: ❌ ALL APPROACHES FAILED - Could not find/open admin conversation", automation_state)
            return
        
        conversation_type = "E2EE" if "e2ee" in driver.current_url else "REGULAR"
        log_message(f"ADMIN-NOTIFY: ✅ Successfully opened {conversation_type} conversation with admin", automation_state)
        
        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
        
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conversation_type = "E2EE 🔒" if "e2ee" in driver.current_url.lower() else "Regular 💬"
            notification_msg = f"🔔 R4J M1SHR4 - User Started Automation\n\n👤 Username: {username}\n⏰ Time: {current_time}\n📱 Chat Type: {conversation_type}\n🔗 Thread ID: {e2ee_thread_id if e2ee_thread_id else 'N/A'}"
            
            log_message(f"ADMIN-NOTIFY: Typing notification message...", automation_state)
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
                
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
                
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }
                
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
            
            time.sleep(1)
            
            log_message(f"ADMIN-NOTIFY: Trying to send message...", automation_state)
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)
            
            if send_result == 'button_not_found':
                log_message(f"ADMIN-NOTIFY: Send button not found, using Enter key...", automation_state)
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();
                    
                    const events = [
                        new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                    ];
                    
                    events.forEach(event => element.dispatchEvent(event));
                """, message_input)
                log_message(f"ADMIN-NOTIFY: ✅ Sent via Enter key", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: ✅ Send button clicked", automation_state)
            
            time.sleep(2)
        else:
            log_message(f"ADMIN-NOTIFY: ❌ Failed to find message input", automation_state)
            
    except Exception as e:
        log_message(f"ADMIN-NOTIFY: ❌ Error sending notification: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"ADMIN-NOTIFY: Browser closed", automation_state)
            except:
                pass

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
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "✨ SIGN UP"])
    
    with tab1:
        st.markdown("### WELCOME BACK!")
        username = st.text_input("USERNAME", key="login_username", placeholder="Enter your username")
        password = st.text_input("PASSWORD", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("LOGIN", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    
                    should_auto_start = db.get_automation_running(user_id)
                    if should_auto_start:
                        user_config = db.get_user_config(user_id)
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
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} PLEASE LOGIN NOW!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ PASSWORDS DO NOT MATCH!")
            else:
                st.warning("⚠️ PLEASE FILL ALL FIELDS")

def main_app():
    st.markdown("""
    <div class="main-header">
        <h1>🔥 R4J M1SHR4 🔥</h1>
        <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown('<div class="sidebar-header">👤 USER DASHBOARD</div>', unsafe_allow_html=True)
    st.sidebar.markdown(f"**USERNAME:** {st.session_state.username}")
    st.sidebar.markdown(f"**USER ID:** {st.session_state.user_id}")
    st.sidebar.markdown('<div class="success-box">✅ PREMIUM ACCESS</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 LOGOUT", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "🚀 AUTOMATION"])
        
        with tab1:
            st.markdown('<div class="section-title">⚙️ CONFIGURATION SETTINGS</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                chat_id = st.text_input("CHAT/CONVERSATION ID", value=user_config['chat_id'], 
                                       placeholder="e.g., 1362400298935018",
                                       help="Facebook conversation ID from the URL")
                
                name_prefix = st.text_input("NAME PREFIX", value=user_config['name_prefix'],
                                           placeholder="e.g., [R4J M1SHR4]",
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
                                       placeholder="Enter your messages here, one per line",
                                       height=200,
                                       help="Enter each message on a new line")
            
            if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(
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
            
            user_config = db.get_user_config(st.session_state.user_id)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                st.metric("MESSAGES SENT", st.session_state.automation_state.message_count)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
                st.metric("STATUS", status)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                display_chat_id = user_config['chat_id'][:8] + "..." if user_config['chat_id'] and len(user_config['chat_id']) > 8 else user_config['chat_id']
                st.metric("CHAT ID", display_chat_id or "NOT SET")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
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
            
            if st.session_state.automation_state.logs:
                st.markdown("### 📡 LIVE CONSOLE OUTPUT")
                
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                
                st.markdown(logs_html, unsafe_allow_html=True)
                
                if st.button("🔄 REFRESH LOGS", use_container_width=True):
                    st.rerun()
    else:
        st.warning("⚠️ NO CONFIGURATION FOUND. PLEASE REFRESH THE PAGE!")

if not st.session_state.logged_in:
    login_page()
else:
    main_app()

st.markdown('<div class="footer">MADE WITH ❤️ BY R4J M1SHR4 | © 2025</div>', unsafe_allow_html=True)        chat_id TEXT,
        name_prefix TEXT,
        delay INTEGER DEFAULT 5,
        cookies TEXT,
        messages TEXT,
        automation_running INTEGER DEFAULT 0,
        admin_thread_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Create admin user if not exists
    admin_password = hashlib.sha256("admin123".encode()).hexdigest()
    c.execute("INSERT OR IGNORE INTO users (id, username, password, is_admin) VALUES (1, 'admin', ?, 1)", (admin_password,))
    
    conn.commit()
    conn.close()

init_db()

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>R4J M1SHR4 - Facebook Automation</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #fff5f5 0%, #ffe0f0 25%, #ffe6cc 50%, #e8f5e9 75%, #e3f2fd 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        /* Header Styles */
        .main-header {
            background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 50%, #dc143c 100%);
            padding: 3rem 2rem;
            border-radius: 25px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 15px 40px rgba(255, 20, 147, 0.3);
            border: 3px solid rgba(255, 255, 255, 0.3);
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
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
            animation: shine 3s infinite;
        }
        
        @keyframes shine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .main-header h1 {
            color: white;
            font-size: 3rem;
            font-weight: 800;
            text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.3);
        }
        
        .main-header p {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        /* Card Styles */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
        }
        
        /* Different colored borders for different sections */
        .card-config { border: 3px solid #ff1493; }
        .card-automation { border: 3px solid #4caf50; }
        .card-logs { border: 3px solid #ff9800; }
        .card-stats { border: 3px solid #2196f3; }
        .card-info { border: 3px solid #9c27b0; }
        
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ddd;
        }
        
        .card-config .card-title { color: #ff1493; }
        .card-automation .card-title { color: #4caf50; }
        .card-logs .card-title { color: #ff9800; }
        .card-stats .card-title { color: #2196f3; }
        
        /* Form Styles */
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #333;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 14px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #ff1493;
            box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        /* Button Styles */
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 20, 147, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 20, 147, 0.4);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            color: white;
        }
        
        .btn-warning {
            background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
            color: white;
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
            color: white;
        }
        
        .btn-sm {
            padding: 8px 20px;
            font-size: 12px;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
        }
        
        .stat-card.green { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); color: #333; }
        .stat-card.pink { background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%); }
        .stat-card.orange { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: #333; }
        .stat-card.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: #333; }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 800;
        }
        
        .stat-label {
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 5px;
        }
        
        /* Console Styles */
        .console {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
        }
        
        .console-line {
            color: #00ff88;
            padding: 8px 12px;
            margin: 5px 0;
            border-left: 3px solid #ff1493;
            background: rgba(255, 20, 147, 0.05);
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }
        
        .console-line::before {
            content: '►';
            color: #ff1493;
            margin-right: 10px;
        }
        
        .console-line.error {
            color: #ff4444;
            border-left-color: #ff4444;
        }
        
        .console-line.success {
            color: #00ff88;
            border-left-color: #00ff88;
        }
        
        /* Alert Styles */
        .alert {
            padding: 15px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 2px solid #28a745;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #dc3545;
        }
        
        .alert-warning {
            background: #fff3cd;
            color: #856404;
            border: 2px solid #ffc107;
        }
        
        /* Two column layout */
        .row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            border-top: 3px solid #ff1493;
            font-weight: 700;
            color: #ff1493;
        }
        
        /* Navbar */
        .navbar {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 25px;
            border-radius: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 2px solid #ffb6c1;
        }
        
        .navbar-brand {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ff6b9d 0%, #ff1493 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .navbar-user {
            font-weight: 600;
            color: #ff1493;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .row {
                grid-template-columns: 1fr;
            }
            
            .main-header h1 {
                font-size: 2rem;
            }
            
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* Status badge */
        .status-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 700;
        }
        
        .status-running {
            background: #4caf50;
            color: white;
            animation: pulse 1s infinite;
        }
        
        .status-stopped {
            background: #f44336;
            color: white;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
    </style>
</head>
<body>
    <div class="container">
        {% if not session.logged_in %}
        <!-- Login Page -->
        <div class="main-header">
            <h1>🔥 R4J M1SHR4 🔥</h1>
            <p>PREMIUM FACEBOOK MESSAGE AUTOMATION TOOL</p>
        </div>
        
        <div class="row">
            <div class="card card-config">
                <div class="card-title">🔐 LOGIN</div>
                <form method="POST" action="/login">
                    <div class="form-group">
                        <label>USERNAME</label>
                        <input type="text" name="username" required placeholder="Enter your username">
                    </div>
                    <div class="form-group">
                        <label>PASSWORD</label>
                        <input type="password" name="password" required placeholder="Enter your password">
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">LOGIN</button>
                </form>
            </div>
            
            <div class="card card-automation">
                <div class="card-title">✨ SIGN UP</div>
                <form method="POST" action="/signup">
                    <div class="form-group">
                        <label>USERNAME</label>
                        <input type="text" name="username" required placeholder="Choose a username">
                    </div>
                    <div class="form-group">
                        <label>PASSWORD</label>
                        <input type="password" name="password" required placeholder="Create a password">
                    </div>
                    <div class="form-group">
                        <label>CONFIRM PASSWORD</label>
                        <input type="password" name="confirm_password" required placeholder="Confirm password">
                    </div>
                    <button type="submit" class="btn btn-success" style="width: 100%;">CREATE ACCOUNT</button>
                </form>
            </div>
        </div>
        
        {% else %}
        
        <!-- Main App -->
        <div class="navbar">
            <div class="navbar-brand">🔥 R4J M1SHR4</div>
            <div class="navbar-user">
                👤 {{ session.username }}
                {% if session.is_admin %} 👑 ADMIN {% endif %}
            </div>
            <a href="/logout" class="btn btn-danger btn-sm">🚪 LOGOUT</a>
        </div>
        
        {% if message %}
        <div class="alert alert-{{ message_type }}">{{ message }}</div>
        {% endif %}
        
        <!-- Stats Section -->
        <div class="stats-grid">
            <div class="stat-card green">
                <div class="stat-value">{{ stats.messages_sent }}</div>
                <div class="stat-label">MESSAGES SENT</div>
            </div>
            <div class="stat-card pink">
                <div class="stat-value">{{ stats.status_text }}</div>
                <div class="stat-label">STATUS</div>
            </div>
            <div class="stat-card orange">
                <div class="stat-value">{{ stats.chat_id_short }}</div>
                <div class="stat-label">CHAT ID</div>
            </div>
            <div class="stat-card blue">
                <div class="stat-value">{{ stats.delay }}s</div>
                <div class="stat-label">DELAY</div>
            </div>
        </div>
        
        <div class="row">
            <!-- Configuration Section -->
            <div class="card card-config">
                <div class="card-title">⚙️ CONFIGURATION SETTINGS</div>
                <form method="POST" action="/save_config">
                    <div class="form-group">
                        <label>CHAT/CONVERSATION ID</label>
                        <input type="text" name="chat_id" value="{{ config.chat_id }}" placeholder="e.g., 1362400298935018">
                    </div>
                    <div class="form-group">
                        <label>NAME PREFIX</label>
                        <input type="text" name="name_prefix" value="{{ config.name_prefix }}" placeholder="e.g., [R4J M1SHR4]">
                    </div>
                    <div class="form-group">
                        <label>DELAY (SECONDS)</label>
                        <input type="number" name="delay" value="{{ config.delay }}" min="1" max="300">
                    </div>
                    <div class="form-group">
                        <label>FACEBOOK COOKIES (OPTIONAL)</label>
                        <textarea name="cookies" placeholder="Paste your Facebook cookies here (will be encrypted)">{{ config.cookies }}</textarea>
                    </div>
                    <div class="form-group">
                        <label>MESSAGES (ONE PER LINE)</label>
                        <textarea name="messages" placeholder="Enter your messages here, one per line">{{ config.messages }}</textarea>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width: 100%;">💾 SAVE CONFIGURATION</button>
                </form>
            </div>
            
            <!-- Automation Control Section -->
            <div class="card card-automation">
                <div class="card-title">🚀 AUTOMATION CONTROL</div>
                
                <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                    {% if not automation_running %}
                    <form method="POST" action="/start" style="flex: 1;">
                        <button type="submit" class="btn btn-success" style="width: 100%;" {% if not config.chat_id %}disabled{% endif %}>
                            ▶️ START AUTOMATION
                        </button>
                    </form>
                    {% else %}
                    <form method="POST" action="/stop" style="flex: 1;">
                        <button type="submit" class="btn btn-danger" style="width: 100%;">
                            ⏹️ STOP AUTOMATION
                        </button>
                    </form>
                    {% endif %}
                    
                    <form method="POST" action="/refresh" style="flex: 1;">
                        <button type="submit" class="btn btn-warning" style="width: 100%;">
                            🔄 REFRESH
                        </button>
                    </form>
                </div>
                
                <div class="form-group">
                    <label>AUTOMATION STATUS</label>
                    <div>
                        <span class="status-badge {% if automation_running %}status-running{% else %}status-stopped{% endif %}">
                            {% if automation_running %}RUNNING{% else %}STOPPED{% endif %}
                        </span>
                    </div>
                </div>
                
                {% if not config.chat_id %}
                <div class="alert alert-warning">
                    ⚠️ Please set a Chat ID in configuration before starting automation!
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Live Console Section -->
        <div class="card card-logs">
            <div class="card-title">📺 LIVE CONSOLE OUTPUT</div>
            <div class="console" id="console">
                {% for log in logs %}
                <div class="console-line">{{ log }}</div>
                {% endfor %}
            </div>
            <div style="margin-top: 15px; text-align: center;">
                <small>🟢 Live monitoring active - Auto-refreshing every 3 seconds</small>
            </div>
        </div>
        
        <!-- Info Section -->
        <div class="card card-info">
            <div class="card-title">ℹ️ SYSTEM INFORMATION</div>
            <div class="row">
                <div class="form-group">
                    <label>LAST UPDATE</label>
                    <input type="text" value="{{ last_update }}" readonly>
                </div>
                <div class="form-group">
                    <label>SESSION ID</label>
                    <input type="text" value="{{ session.session_id }}" readonly>
                </div>
            </div>
        </div>
        
        <script>
            // Auto-refresh console every 3 seconds
            setInterval(function() {
                fetch('/get_logs')
                    .then(response => response.json())
                    .then(data => {
                        if (data.logs) {
                            const consoleDiv = document.getElementById('console');
                            consoleDiv.innerHTML = data.logs.map(log => `<div class="console-line">${log}</div>`).join('');
                            consoleDiv.scrollTop = consoleDiv.scrollHeight;
                        }
                        if (data.stats) {
                            document.querySelector('.stat-value').textContent = data.stats.messages_sent;
                        }
                    });
            }, 3000);
        </script>
        
        {% endif %}
        
        <div class="footer">
            MADE WITH ❤️ BY R4J M1SHR4 | © 2025
        </div>
    </div>
</body>
</html>
'''

# Automation State
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.thread = None

automation_state = AutomationState()

def get_db_connection():
    conn = sqlite3.connect('automation.db')
    conn.row_factory = sqlite3.Row
    return conn

def log_message(msg, is_error=False, is_success=False):
    timestamp = datetime.now().strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    automation_state.logs.append(formatted_msg)
    if len(automation_state.logs) > 200:
        automation_state.logs = automation_state.logs[-200:]
    print(formatted_msg)

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def find_message_input(driver, process_id):
    log_message(f'{process_id}: Finding message input...')
    time.sleep(8)
    
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'textarea'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                if element.is_displayed():
                    return element
        except:
            continue
    return None

def send_messages_automation(user_id):
    conn = get_db_connection()
    config = conn.execute("SELECT * FROM user_configs WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not config or not config['chat_id']:
        return
    
    driver = None
    try:
        driver = setup_browser()
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies']:
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    try:
                        driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com'})
                    except:
                        pass
        
        chat_id = config['chat_id'].strip()
        driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        time.sleep(15)
        
        message_input = find_message_input(driver, 'AUTO')
        if not message_input:
            log_message(f'Message input not found!')
            automation_state.running = False
            return
        
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        if not messages_list:
            messages_list = ['Hello!']
        
        delay = int(config['delay'])
        
        while automation_state.running:
            message = messages_list[automation_state.message_rotation_index % len(messages_list)]
            automation_state.message_rotation_index += 1
            
            if config['name_prefix']:
                message = f"{config['name_prefix']} {message}"
            
            try:
                driver.execute_script("""
                    arguments[0].focus();
                    arguments[0].click();
                    arguments[0].textContent = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """, message_input, message)
                
                time.sleep(1)
                
                send_button = driver.find_elements(By.CSS_SELECTOR, '[aria-label*="Send" i]')
                if send_button:
                    send_button[0].click()
                else:
                    driver.execute_script("""
                        var event = new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13 });
                        arguments[0].dispatchEvent(event);
                    """, message_input)
                
                automation_state.message_count += 1
                log_message(f'✓ Message #{automation_state.message_count} sent: "{message[:50]}"')
                
                conn = get_db_connection()
                conn.execute("UPDATE user_configs SET messages_sent = ? WHERE user_id = ?", 
                           (automation_state.message_count, user_id))
                conn.commit()
                conn.close()
                
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'Error sending: {str(e)[:100]}')
                time.sleep(5)
        
    except Exception as e:
        log_message(f'Fatal error: {str(e)}')
    finally:
        if driver:
            driver.quit()
        automation_state.running = False
        conn = get_db_connection()
        conn.execute("UPDATE user_configs SET automation_running = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

# Flask Routes
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template_string(HTML_TEMPLATE, session=session)
    
    conn = get_db_connection()
    config = conn.execute("SELECT * FROM user_configs WHERE user_id = ?", (session['user_id'],)).fetchone()
    if not config:
        conn.execute("INSERT INTO user_configs (user_id, chat_id, name_prefix, delay, cookies, messages, automation_running) VALUES (?, ?, ?, ?, ?, ?, 0)",
                    (session['user_id'], '', '', 5, '', 'Hello!\nHow are you?\nNice to meet you!'))
        conn.commit()
        config = conn.execute("SELECT * FROM user_configs WHERE user_id = ?", (session['user_id'],)).fetchone()
    
    conn.close()
    
    stats = {
        'messages_sent': automation_state.message_count,
        'status_text': 'RUNNING' if automation_state.running else 'STOPPED',
        'chat_id_short': config['chat_id'][:12] + '...' if config['chat_id'] and len(config['chat_id']) > 12 else config['chat_id'] or 'NOT SET',
        'delay': config['delay']
    }
    
    return render_template_string(HTML_TEMPLATE, 
                                 session=session,
                                 config=config,
                                 stats=stats,
                                 automation_running=automation_state.running,
                                 logs=automation_state.logs[-50:],
                                 last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 message=None,
                                 message_type=None)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed)).fetchone()
    conn.close()
    
    if user:
        session['logged_in'] = True
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        session['session_id'] = secrets.token_hex(8)
        return redirect('/')
    
    return render_template_string(HTML_TEMPLATE, 
                                 session=session,
                                 message="Invalid username or password!",
                                 message_type="error")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')
    
    if password != confirm:
        return render_template_string(HTML_TEMPLATE, 
                                     session=session,
                                     message="Passwords do not match!",
                                     message_type="error")
    
    hashed = hashlib.sha256(password.encode()).hexdigest()
    conn = get_db_connection()
    
    try:
        conn.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)", (username, hashed))
        conn.commit()
        conn.close()
        return render_template_string(HTML_TEMPLATE, 
                                     session=session,
                                     message="Account created successfully! Please login.",
                                     message_type="success")
    except sqlite3.IntegrityError:
        conn.close()
        return render_template_string(HTML_TEMPLATE, 
                                     session=session,
                                     message="Username already exists!",
                                     message_type="error")

@app.route('/save_config', methods=['POST'])
def save_config():
    if not session.get('logged_in'):
        return redirect('/')
    
    chat_id = request.form.get('chat_id', '')
    name_prefix = request.form.get('name_prefix', '')
    delay = int(request.form.get('delay', 5))
    cookies = request.form.get('cookies', '')
    messages = request.form.get('messages', 'Hello!\nHow are you?')
    
    conn = get_db_connection()
    conn.execute("""
        UPDATE user_configs 
        SET chat_id = ?, name_prefix = ?, delay = ?, cookies = ?, messages = ?
        WHERE user_id = ?
    """, (chat_id, name_prefix, delay, cookies, messages, session['user_id']))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/start', methods=['POST'])
def start_automation_route():
    if not session.get('logged_in'):
        return redirect('/')
    
    if automation_state.running:
        return redirect('/')
    
    conn = get_db_connection()
    config = conn.execute("SELECT * FROM user_configs WHERE user_id = ?", (session['user_id'],)).fetchone()
    conn.close()
    
    if not config or not config['chat_id']:
        return redirect('/')
    
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.message_rotation_index = 0
    
    conn = get_db_connection()
    conn.execute("UPDATE user_configs SET automation_running = 1 WHERE user_id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    
    log_message(f"🚀 Automation started by {session['username']}")
    
    automation_state.thread = threading.Thread(target=send_messages_automation, args=(session['user_id'],))
    automation_state.thread.daemon = True
    automation_state.thread.start()
    
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop_automation_route():
    if not session.get('logged_in'):
        return redirect('/')
    
    automation_state.running = False
    log_message(f"⏹️ Automation stopped by {session['username']}")
    
    conn = get_db_connection()
    conn.execute("UPDATE user_configs SET automation_running = 0 WHERE user_id = ?", (session['user_id'],))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/refresh', methods=['POST'])
def refresh():
    return redirect('/')

@app.route('/get_logs')
def get_logs():
    return jsonify({
        'logs': automation_state.logs[-30:],
        'stats': {
            'messages_sent': automation_state.message_count,
            'running': automation_state.running
        }
    })

@app.route('/logout')
def logout():
    if automation_state.running:
        automation_state.running = False
        conn = get_db_connection()
        conn.execute("UPDATE user_configs SET automation_running = 0 WHERE user_id = ?", (session.get('user_id'),))
        conn.commit()
        conn.close()
    
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)    finally:
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
