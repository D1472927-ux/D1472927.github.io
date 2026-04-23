"""
donation.py — 捐獻紀錄資料模型

對應資料表：donations
功能：記錄使用者的香油錢捐獻意向

注意：MVP 階段僅模擬捐獻流程，不串接真實金流。
"""

import sqlite3
from app.models.db import get_connection


def create(user_id, amount, wish=None, is_anonymous=0):
    """新增一筆捐獻紀錄。"""
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO donations (user_id, amount, wish, is_anonymous)
               VALUES (?, ?, ?, ?)''',
            (user_id, amount, wish, is_anonymous)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f'[ERROR] Create donation failed: {e}')
        return None
    finally:
        conn.close()


def get_all():
    """取得所有捐獻紀錄（匿名捐獻隱藏使用者名稱）。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            '''SELECT d.*, u.username
               FROM donations d
               JOIN users u ON d.user_id = u.id
               ORDER BY d.created_at DESC'''
        ).fetchall()
        result = []
        for row in rows:
            record = dict(row)
            if record['is_anonymous']:
                record['username'] = 'Anonymous'
            result.append(record)
        return result
    except sqlite3.Error as e:
        print(f'[ERROR] Query donations failed: {e}')
        return []
    finally:
        conn.close()


def get_by_id(donation_id):
    """依 ID 取得特定捐獻紀錄。"""
    conn = get_connection()
    try:
        row = conn.execute(
            '''SELECT d.*, u.username
               FROM donations d
               JOIN users u ON d.user_id = u.id
               WHERE d.id = ?''',
            (donation_id,)
        ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f'[ERROR] Query donation ID={donation_id} failed: {e}')
        return None
    finally:
        conn.close()


def get_by_user(user_id):
    """取得特定使用者的所有捐獻紀錄。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            '''SELECT * FROM donations
               WHERE user_id = ?
               ORDER BY created_at DESC''',
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query user donations failed: {e}')
        return []
    finally:
        conn.close()


def get_user_total(user_id):
    """取得特定使用者的捐獻總額。"""
    conn = get_connection()
    try:
        result = conn.execute(
            'SELECT COALESCE(SUM(amount), 0) FROM donations WHERE user_id = ?',
            (user_id,)
        ).fetchone()
        return result[0]
    except sqlite3.Error as e:
        print(f'[ERROR] Query donation total failed: {e}')
        return 0
    finally:
        conn.close()


def update(donation_id, amount=None, wish=None, is_anonymous=None):
    """更新捐獻紀錄。"""
    fields = []
    values = []
    if amount is not None:
        fields.append('amount = ?')
        values.append(amount)
    if wish is not None:
        fields.append('wish = ?')
        values.append(wish)
    if is_anonymous is not None:
        fields.append('is_anonymous = ?')
        values.append(is_anonymous)
    if not fields:
        return False

    values.append(donation_id)
    sql = f'UPDATE donations SET {", ".join(fields)} WHERE id = ?'
    conn = get_connection()
    try:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Update donation ID={donation_id} failed: {e}')
        return False
    finally:
        conn.close()


def delete(donation_id):
    """刪除捐獻紀錄。"""
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM donations WHERE id = ?', (donation_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Delete donation ID={donation_id} failed: {e}')
        return False
    finally:
        conn.close()
