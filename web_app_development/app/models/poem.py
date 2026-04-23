"""
poem.py — 籤詩資料模型

對應資料表：poems
功能：籤詩的查詢與管理，核心方法為隨機抽籤
"""

import sqlite3
from app.models.db import get_connection


def create(category, level, title, poem_text, interpretation):
    """新增一支籤詩。"""
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO poems (category, level, title, poem_text, interpretation)
               VALUES (?, ?, ?, ?, ?)''',
            (category, level, title, poem_text, interpretation)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f'[ERROR] Create poem failed: {e}')
        return None
    finally:
        conn.close()


def get_all():
    """取得所有籤詩。"""
    conn = get_connection()
    try:
        rows = conn.execute('SELECT * FROM poems ORDER BY id').fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query poems failed: {e}')
        return []
    finally:
        conn.close()


def get_by_id(poem_id):
    """依 ID 取得特定籤詩。"""
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM poems WHERE id = ?', (poem_id,)
        ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f'[ERROR] Query poem ID={poem_id} failed: {e}')
        return None
    finally:
        conn.close()


def get_by_category(category):
    """依類別取得所有籤詩。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM poems WHERE category = ? ORDER BY id',
            (category,)
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query poems by category failed: {e}')
        return []
    finally:
        conn.close()


def get_random(category=None):
    """隨機取得一支籤詩（核心抽籤邏輯）。"""
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
    except sqlite3.Error as e:
        print(f'[ERROR] Random draw failed: {e}')
        return None
    finally:
        conn.close()


def get_categories():
    """取得所有可用的籤詩類別。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT DISTINCT category FROM poems ORDER BY category'
        ).fetchall()
        return [row['category'] for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query categories failed: {e}')
        return []
    finally:
        conn.close()


def update(poem_id, category=None, level=None, title=None,
           poem_text=None, interpretation=None):
    """更新籤詩資料。"""
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
    except sqlite3.Error as e:
        print(f'[ERROR] Update poem ID={poem_id} failed: {e}')
        return False
    finally:
        conn.close()


def delete(poem_id):
    """刪除籤詩。"""
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM poems WHERE id = ?', (poem_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Delete poem ID={poem_id} failed: {e}')
        return False
    finally:
        conn.close()
