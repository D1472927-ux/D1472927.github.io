"""
poem.py — 籤詩資料模型

對應資料表：poems
功能：籤詩的查詢與管理，核心方法為隨機抽籤

籤詩屬於靜態參考資料，主要透過 seed.sql 匯入，
一般不需要在應用程式中手動新增。
"""

from app.models.db import get_connection


def create(category, level, title, poem_text, interpretation):
    """
    新增一支籤詩。

    Args:
        category (str): 類別（事業/感情/學業/健康/財運）
        level (str): 籤等級（上上籤/上籤/中籤/下籤/下下籤）
        title (str): 籤題
        poem_text (str): 籤詩原文
        interpretation (str): 白話文解釋

    Returns:
        int: 新建立的籤詩 ID
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO poems (category, level, title, poem_text, interpretation)
               VALUES (?, ?, ?, ?, ?)''',
            (category, level, title, poem_text, interpretation)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all():
    """
    取得所有籤詩。

    Returns:
        list[dict]: 所有籤詩清單
    """
    conn = get_connection()
    try:
        rows = conn.execute('SELECT * FROM poems ORDER BY id').fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_by_id(poem_id):
    """
    依 ID 取得特定籤詩。

    Args:
        poem_id (int): 籤詩 ID

    Returns:
        dict or None: 籤詩資料，若不存在回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM poems WHERE id = ?', (poem_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_by_category(category):
    """
    依類別取得所有籤詩。

    Args:
        category (str): 類別名稱

    Returns:
        list[dict]: 該類別的籤詩清單
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM poems WHERE category = ? ORDER BY id',
            (category,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_random(category=None):
    """
    隨機取得一支籤詩（核心抽籤邏輯）。

    可指定類別篩選，若不指定則從所有籤詩中隨機抽取。

    Args:
        category (str, optional): 限定的類別

    Returns:
        dict or None: 隨機選中的籤詩，若無資料回傳 None
    """
    conn = get_connection()
    try:
        if category:
            row = conn.execute(
                'SELECT * FROM poems WHERE category = ? ORDER BY RANDOM() LIMIT 1',
                (category,)
            ).fetchone()
        else:
            row = conn.execute(
                'SELECT * FROM poems ORDER BY RANDOM() LIMIT 1'
            ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_categories():
    """
    取得所有可用的籤詩類別。

    Returns:
        list[str]: 類別名稱清單（如 ['事業', '感情', '學業', '健康', '財運']）
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT DISTINCT category FROM poems ORDER BY category'
        ).fetchall()
        return [row['category'] for row in rows]
    finally:
        conn.close()


def update(poem_id, category=None, level=None, title=None,
           poem_text=None, interpretation=None):
    """
    更新籤詩資料。

    Args:
        poem_id (int): 籤詩 ID
        category (str, optional): 新類別
        level (str, optional): 新等級
        title (str, optional): 新籤題
        poem_text (str, optional): 新籤詩原文
        interpretation (str, optional): 新白話文解釋

    Returns:
        bool: 是否更新成功
    """
    fields = []
    values = []

    if category is not None:
        fields.append('category = ?')
        values.append(category)
    if level is not None:
        fields.append('level = ?')
        values.append(level)
    if title is not None:
        fields.append('title = ?')
        values.append(title)
    if poem_text is not None:
        fields.append('poem_text = ?')
        values.append(poem_text)
    if interpretation is not None:
        fields.append('interpretation = ?')
        values.append(interpretation)

    if not fields:
        return False

    values.append(poem_id)
    sql = f'UPDATE poems SET {", ".join(fields)} WHERE id = ?'

    conn = get_connection()
    try:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete(poem_id):
    """
    刪除籤詩。

    Args:
        poem_id (int): 籤詩 ID

    Returns:
        bool: 是否刪除成功
    """
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM poems WHERE id = ?', (poem_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
