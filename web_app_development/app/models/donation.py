"""
donation.py — 捐獻紀錄資料模型

對應資料表：donations
功能：記錄使用者的香油錢捐獻意向

注意：MVP 階段僅模擬捐獻流程，不串接真實金流。
"""

from app.models.db import get_connection


def create(user_id, amount, wish=None, is_anonymous=0):
    """
    新增一筆捐獻紀錄。

    Args:
        user_id (int): 使用者 ID（捐獻需登入）
        amount (int): 捐獻金額（新台幣，正整數）
        wish (str, optional): 祈願內容
        is_anonymous (int): 是否匿名（0=具名, 1=匿名）

    Returns:
        int: 新建立的捐獻紀錄 ID
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO donations (user_id, amount, wish, is_anonymous)
               VALUES (?, ?, ?, ?)''',
            (user_id, amount, wish, is_anonymous)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all():
    """
    取得所有捐獻紀錄（匿名捐獻的使用者名稱會被遮蔽）。

    Returns:
        list[dict]: 所有捐獻紀錄（依建立時間降冪排列）
    """
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
            # 匿名捐獻隱藏使用者名稱
            if record['is_anonymous']:
                record['username'] = '匿名善心人士'
            result.append(record)
        return result
    finally:
        conn.close()


def get_by_id(donation_id):
    """
    依 ID 取得特定捐獻紀錄。

    Args:
        donation_id (int): 捐獻紀錄 ID

    Returns:
        dict or None: 捐獻紀錄資料，若不存在回傳 None
    """
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
    finally:
        conn.close()


def get_by_user(user_id):
    """
    取得特定使用者的所有捐獻紀錄。

    Args:
        user_id (int): 使用者 ID

    Returns:
        list[dict]: 該使用者的捐獻紀錄清單
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            '''SELECT * FROM donations
               WHERE user_id = ?
               ORDER BY created_at DESC''',
            (user_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_user_total(user_id):
    """
    取得特定使用者的捐獻總額。

    Args:
        user_id (int): 使用者 ID

    Returns:
        int: 捐獻總額（新台幣）
    """
    conn = get_connection()
    try:
        result = conn.execute(
            'SELECT COALESCE(SUM(amount), 0) FROM donations WHERE user_id = ?',
            (user_id,)
        ).fetchone()
        return result[0]
    finally:
        conn.close()


def update(donation_id, amount=None, wish=None, is_anonymous=None):
    """
    更新捐獻紀錄。

    Args:
        donation_id (int): 捐獻紀錄 ID
        amount (int, optional): 新金額
        wish (str, optional): 新祈願內容
        is_anonymous (int, optional): 新匿名設定

    Returns:
        bool: 是否更新成功
    """
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
    finally:
        conn.close()


def delete(donation_id):
    """
    刪除捐獻紀錄。

    Args:
        donation_id (int): 捐獻紀錄 ID

    Returns:
        bool: 是否刪除成功
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            'DELETE FROM donations WHERE id = ?', (donation_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
