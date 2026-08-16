import sqlite3
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
import hashlib
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(BASE_DIR, "backend", "api", "repositories", "fitness.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            password TEXT NOT NULL,
            token TEXT,
            subscription_id TEXT,
            subscription_end TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            plan_type TEXT NOT NULL,
            price REAL NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            subscription_id TEXT,
            payment_id TEXT,
            amount REAL NOT NULL,
            payment_method TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    try:
        cursor.execute('ALTER TABLE payments ADD COLUMN payment_id TEXT')
    except:
        pass

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def verify_password(password: str, hashed: str) -> bool:
    try:
        hash_part, salt = hashed.split(':')
        return hash_part == hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    except:
        return False


def generate_token() -> str:
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()


def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_user(name: str, email: str, phone: str, password: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)
        token = generate_token()
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO users (id, name, email, phone, password, token, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, name.strip(), email.strip().lower(), phone.strip(), hashed_password, token, now, now))

        conn.commit()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return dict(user)
        return None
    except sqlite3.IntegrityError:
        conn.close()
        return None
    except Exception as e:
        conn.close()
        return None


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email.strip().lower(),))
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None


def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE token = ?', (token,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None


def update_user_token(user_id: str) -> Optional[str]:
    conn = get_db_connection()
    cursor = conn.cursor()

    new_token = generate_token()
    now = datetime.now().isoformat()

    cursor.execute('''
        UPDATE users SET token = ?, updated_at = ? WHERE id = ?
    ''', (new_token, now, user_id))

    conn.commit()
    conn.close()

    return new_token


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, name, email, phone, subscription_id, subscription_end, created_at FROM users WHERE id = ?',
        (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)
    return None


def create_subscription(user_id: str, plan_type: str, price: float, duration_days: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sub_id = str(uuid.uuid4())
        start_date = datetime.now().isoformat()
        end_date = (datetime.now() + timedelta(days=duration_days)).isoformat()
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO subscriptions (id, user_id, plan_type, price, start_date, end_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sub_id, user_id, plan_type, price, start_date, end_date, now))

        cursor.execute('''
            UPDATE users SET subscription_id = ?, subscription_end = ? WHERE id = ?
        ''', (sub_id, end_date, user_id))

        conn.commit()

        cursor.execute('SELECT * FROM subscriptions WHERE id = ?', (sub_id,))
        subscription = cursor.fetchone()
        conn.close()

        if subscription:
            return dict(subscription)
        return None
    except Exception as e:
        conn.close()
        return None


def get_user_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM subscriptions 
        WHERE user_id = ?
        ORDER BY end_date DESC LIMIT 1
    ''', (user_id,))

    subscription = cursor.fetchone()
    conn.close()

    if subscription:
        return dict(subscription)
    return None


def cancel_subscription(subscription_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE subscriptions SET status = 'cancelled' WHERE id = ?
        ''', (subscription_id,))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False


def refund_subscription(subscription_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE subscriptions SET status = 'refunded' WHERE id = ?
        ''', (subscription_id,))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False


def create_payment(user_id: str, subscription_id: str, amount: float, payment_method: str = 'card') -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        payment_id = str(uuid.uuid4())
        now = datetime.now().isoformat()

        cursor.execute('''
            INSERT INTO payments (id, user_id, subscription_id, amount, payment_method, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'completed', ?)
        ''', (payment_id, user_id, subscription_id, amount, payment_method, now))

        conn.commit()

        cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
        payment = cursor.fetchone()
        conn.close()

        if payment:
            return dict(payment)
        return None
    except Exception as e:
        conn.close()
        return None


def update_payment_subscription(payment_record_id: str, yookassa_payment_id: str) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE payments SET payment_id = ? WHERE id = ?
        ''', (yookassa_payment_id, payment_record_id))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False


def get_payment_by_subscription_id(subscription_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM payments WHERE subscription_id = ?', (subscription_id,))
    payment = cursor.fetchone()
    conn.close()

    if payment:
        return dict(payment)
    return None