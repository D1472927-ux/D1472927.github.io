"""
user.py — 使用者資料模型

對應資料表：users
功能：使用者註冊、登入驗證、個人資訊查詢

安全注意：
- 密碼使用 werkzeug.security 進行雜湊，禁止明文儲存
- 所有 SQL 查詢使用參數化語法（? 佔位符），防止 SQL Injection
"""

from werkzeug.security import generate_password_hash, check_password_hash
from app.models.db import get_connection


def create(username, password):
    """
    建立新使用者。

    Args:
        username (str): 使用者帳號
        password (str): 使用者密碼（明文，會自動雜湊）

    Returns:
        int: 新建立的使用者 ID

    Raises:
        sqlite3.IntegrityError: 若 username 已存在
    """
    password_hash = generate_password_hash(password)
    conn = get_connection()
    try:
        cursor = conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, password_hash)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all():
    """
    取得所有使用者（不含密碼雜湊）。

    Returns:
        list[dict]: 使用者清單
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT id, username, created_at FROM users ORDER BY id'
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_by_id(user_id):
    """
    依 ID 取得使用者資料。

    Args:
        user_id (int): 使用者 ID

    Returns:
        dict or None: 使用者資料（不含密碼雜湊），若不存在回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT id, username, created_at FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_by_username(username):
    """
    依帳號取得使用者資料（含密碼雜湊，供登入驗證用）。

    Args:
        username (str): 使用者帳號

    Returns:
        dict or None: 使用者完整資料，若不存在回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def verify_password(username, password):
    """
    驗證使用者的帳號與密碼。

    Args:
        username (str): 使用者帳號
        password (str): 使用者密碼（明文）

    Returns:
        dict or None: 驗證成功回傳使用者資料（不含密碼），失敗回傳 None
    """
    user = get_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return {
            'id': user['id'],
            'username': user['username'],
            'created_at': user['created_at']
        }
    return None


def update(user_id, username=None, password=None):
    """
    更新使用者資料。

    Args:
        user_id (int): 使用者 ID
        username (str, optional): 新的使用者帳號
        password (str, optional): 新的密碼（明文，會自動雜湊）

    Returns:
        bool: 是否更新成功
    """
    fields = []
    values = []

    if username is not None:
        fields.append('username = ?')
        values.append(username)
    if password is not None:
        fields.append('password_hash = ?')
        values.append(generate_password_hash(password))

    if not fields:
        return False

    values.append(user_id)
    sql = f'UPDATE users SET {", ".join(fields)} WHERE id = ?'

    conn = get_connection()
    try:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete(user_id):
    """
    刪除使用者。

    Args:
        user_id (int): 使用者 ID

    Returns:
        bool: 是否刪除成功
    """
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def get_stats(user_id):
    """
    取得使用者的統計資料（用於個人中心頁面）。

    Args:
        user_id (int): 使用者 ID

    Returns:
        dict: 包含 fortune_count（算命次數）、donation_total（捐獻總額）
    """
    conn = get_connection()
    try:
        fortune_count = conn.execute(
            'SELECT COUNT(*) FROM fortunes WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0]

        donation_total = conn.execute(
            'SELECT COALESCE(SUM(amount), 0) FROM donations WHERE user_id = ?',
            (user_id,)
        ).fetchone()[0]

        return {
            'fortune_count': fortune_count,
            'donation_total': donation_total
        }
    finally:
        conn.close()
