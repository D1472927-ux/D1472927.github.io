"""
tarot.py — 塔羅牌資料模型

對應資料表：tarot_cards
功能：塔羅牌的查詢與管理，核心方法為隨機抽牌
"""

import sqlite3
import random
from app.models.db import get_connection


def create(name, upright_meaning, reversed_meaning,
           upright_description, reversed_description, image_url=None):
    """新增一張塔羅牌。"""
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO tarot_cards
               (name, image_url, upright_meaning, reversed_meaning,
                upright_description, reversed_description)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (name, image_url, upright_meaning, reversed_meaning,
             upright_description, reversed_description)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f'[ERROR] Create tarot card failed: {e}')
        return None
    finally:
        conn.close()


def get_all():
    """取得所有塔羅牌。"""
    conn = get_connection()
    try:
        rows = conn.execute('SELECT * FROM tarot_cards ORDER BY id').fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query tarot cards failed: {e}')
        return []
    finally:
        conn.close()


def get_by_id(card_id):
    """依 ID 取得特定塔羅牌。"""
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM tarot_cards WHERE id = ?', (card_id,)
        ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f'[ERROR] Query tarot card ID={card_id} failed: {e}')
        return None
    finally:
        conn.close()


def draw_cards(count=1):
    """隨機抽取指定數量的塔羅牌，並決定正位/逆位。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM tarot_cards ORDER BY RANDOM() LIMIT ?',
            (count,)
        ).fetchall()

        result = []
        for row in rows:
            card = dict(row)
            is_reversed = random.choice([True, False])
            result.append({
                'card': card,
                'is_reversed': is_reversed,
                'meaning': card['reversed_meaning'] if is_reversed else card['upright_meaning'],
                'description': card['reversed_description'] if is_reversed else card['upright_description']
            })
        return result
    except sqlite3.Error as e:
        print(f'[ERROR] Draw cards failed: {e}')
        return []
    finally:
        conn.close()


def update(card_id, name=None, image_url=None, upright_meaning=None,
           reversed_meaning=None, upright_description=None,
           reversed_description=None):
    """更新塔羅牌資料。"""
    fields = []
    values = []
    if name is not None:
        fields.append('name = ?')
        values.append(name)
    if image_url is not None:
        fields.append('image_url = ?')
        values.append(image_url)
    if upright_meaning is not None:
        fields.append('upright_meaning = ?')
        values.append(upright_meaning)
    if reversed_meaning is not None:
        fields.append('reversed_meaning = ?')
        values.append(reversed_meaning)
    if upright_description is not None:
        fields.append('upright_description = ?')
        values.append(upright_description)
    if reversed_description is not None:
        fields.append('reversed_description = ?')
        values.append(reversed_description)
    if not fields:
        return False

    values.append(card_id)
    sql = f'UPDATE tarot_cards SET {", ".join(fields)} WHERE id = ?'
    conn = get_connection()
    try:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Update tarot card ID={card_id} failed: {e}')
        return False
    finally:
        conn.close()


def delete(card_id):
    """刪除塔羅牌。"""
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM tarot_cards WHERE id = ?', (card_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Delete tarot card ID={card_id} failed: {e}')
        return False
    finally:
        conn.close()
