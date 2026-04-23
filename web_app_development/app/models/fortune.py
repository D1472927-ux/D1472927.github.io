"""
fortune.py — 算命結果資料模型

對應資料表：fortunes
功能：儲存與查詢所有抽籤 / 塔羅占卜的結果紀錄
"""

import sqlite3
import uuid
import json
from app.models.db import get_connection


def create(type, category=None, question=None, poem_id=None,
           tarot_cards_json=None, result_summary=None, user_id=None):
    """新增一筆算命結果。"""
    share_token = str(uuid.uuid4())
    conn = get_connection()
    try:
        cursor = conn.execute(
            '''INSERT INTO fortunes
               (user_id, type, category, question, poem_id,
                tarot_cards_json, result_summary, share_token)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (user_id, type, category, question, poem_id,
             tarot_cards_json, result_summary, share_token)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f'[ERROR] Create fortune failed: {e}')
        return None
    finally:
        conn.close()


def get_all():
    """取得所有算命紀錄。"""
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM fortunes ORDER BY created_at DESC'
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query fortunes failed: {e}')
        return []
    finally:
        conn.close()


def get_by_id(fortune_id):
    """依 ID 取得特定算命紀錄（含 JOIN 籤詩資料）。"""
    conn = get_connection()
    try:
        row = conn.execute(
            '''SELECT f.*, p.category AS poem_category, p.level AS poem_level,
                      p.title AS poem_title, p.poem_text, p.interpretation
               FROM fortunes f
               LEFT JOIN poems p ON f.poem_id = p.id
               WHERE f.id = ?''',
            (fortune_id,)
        ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f'[ERROR] Query fortune ID={fortune_id} failed: {e}')
        return None
    finally:
        conn.close()


def get_by_user(user_id, type_filter=None, date_from=None):
    """取得特定使用者的算命紀錄（支援篩選）。"""
    conditions = ['f.user_id = ?']
    params = [user_id]
    if type_filter:
        conditions.append('f.type = ?')
        params.append(type_filter)
    if date_from:
        conditions.append('f.created_at >= ?')
        params.append(date_from)
    where_clause = ' AND '.join(conditions)

    conn = get_connection()
    try:
        rows = conn.execute(
            f'''SELECT f.*, p.level AS poem_level, p.title AS poem_title
                FROM fortunes f
                LEFT JOIN poems p ON f.poem_id = p.id
                WHERE {where_clause}
                ORDER BY f.created_at DESC''',
            params
        ).fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f'[ERROR] Query user fortunes failed: {e}')
        return []
    finally:
        conn.close()


def get_by_share_token(share_token):
    """依分享 token 取得算命結果。"""
    conn = get_connection()
    try:
        row = conn.execute(
            '''SELECT f.*, p.category AS poem_category, p.level AS poem_level,
                      p.title AS poem_title, p.poem_text, p.interpretation
               FROM fortunes f
               LEFT JOIN poems p ON f.poem_id = p.id
               WHERE f.share_token = ?''',
            (share_token,)
        ).fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f'[ERROR] Query share token failed: {e}')
        return None
    finally:
        conn.close()


def update(fortune_id, user_id=None, result_summary=None):
    """更新算命紀錄。"""
    fields = []
    values = []
    if user_id is not None:
        fields.append('user_id = ?')
        values.append(user_id)
    if result_summary is not None:
        fields.append('result_summary = ?')
        values.append(result_summary)
    if not fields:
        return False

    values.append(fortune_id)
    sql = f'UPDATE fortunes SET {", ".join(fields)} WHERE id = ?'
    conn = get_connection()
    try:
        cursor = conn.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Update fortune ID={fortune_id} failed: {e}')
        return False
    finally:
        conn.close()


def delete(fortune_id):
    """刪除算命紀錄。"""
    conn = get_connection()
    try:
        cursor = conn.execute('DELETE FROM fortunes WHERE id = ?', (fortune_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f'[ERROR] Delete fortune ID={fortune_id} failed: {e}')
        return False
    finally:
        conn.close()


def parse_tarot_json(tarot_cards_json):
    """解析塔羅牌結果的 JSON 字串。"""
    if not tarot_cards_json:
        return []
    try:
        return json.loads(tarot_cards_json)
    except (json.JSONDecodeError, TypeError):
        return []
