"""
fortune.py — 算命結果資料模型

對應資料表：fortunes
功能：儲存與查詢所有抽籤 / 塔羅占卜的結果紀錄

此模型是系統的核心紀錄表，整合了：
- 抽籤結果（關聯 poems 表）
- 塔羅結果（以 JSON 儲存抽到的牌）
- 分享功能（透過 share_token）
- 歷史紀錄查詢（支援篩選）
"""

import uuid
import json
from app.models.db import get_connection


def create(type, category=None, question=None, poem_id=None,
           tarot_cards_json=None, result_summary=None, user_id=None):
    """
    新增一筆算命結果。

    Args:
        type (str): 算命類型（'draw' 或 'tarot'）
        category (str, optional): 詢問類別或占卜主題
        question (str, optional): 使用者的問題
        poem_id (int, optional): 關聯的籤詩 ID（抽籤用）
        tarot_cards_json (str, optional): 塔羅結果 JSON 字串
        result_summary (str, optional): 結果摘要
        user_id (int, optional): 使用者 ID（未登入時為 None）

    Returns:
        int: 新建立的紀錄 ID
    """
    # 自動產生分享用的唯一 token
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
    finally:
        conn.close()


def get_all():
    """
    取得所有算命紀錄。

    Returns:
        list[dict]: 所有紀錄清單（依建立時間降冪排列）
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM fortunes ORDER BY created_at DESC'
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_by_id(fortune_id):
    """
    依 ID 取得特定算命紀錄。

    若為抽籤類型，會一併 JOIN 取得籤詩資料。

    Args:
        fortune_id (int): 紀錄 ID

    Returns:
        dict or None: 紀錄資料，若不存在回傳 None
    """
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
    finally:
        conn.close()


def get_by_user(user_id, type_filter=None, date_from=None):
    """
    取得特定使用者的算命紀錄（支援篩選）。

    Args:
        user_id (int): 使用者 ID
        type_filter (str, optional): 篩選類型（'draw' 或 'tarot'）
        date_from (str, optional): 篩選起始日期（ISO 格式，如 '2026-04-01'）

    Returns:
        list[dict]: 該使用者的紀錄清單（依建立時間降冪排列）
    """
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
    finally:
        conn.close()


def get_by_share_token(share_token):
    """
    依分享 token 取得算命結果（用於分享頁面）。

    Args:
        share_token (str): 分享用的唯一 token

    Returns:
        dict or None: 紀錄資料（含籤詩），若不存在回傳 None
    """
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
    finally:
        conn.close()


def update(fortune_id, user_id=None, result_summary=None):
    """
    更新算命紀錄。

    主要用途：
    - 將未登入時的紀錄關聯到使用者（登入後補存）
    - 更新結果摘要

    Args:
        fortune_id (int): 紀錄 ID
        user_id (int, optional): 要關聯的使用者 ID
        result_summary (str, optional): 新的結果摘要

    Returns:
        bool: 是否更新成功
    """
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
    finally:
        conn.close()


def delete(fortune_id):
    """
    刪除算命紀錄。

    Args:
        fortune_id (int): 紀錄 ID

    Returns:
        bool: 是否刪除成功
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            'DELETE FROM fortunes WHERE id = ?', (fortune_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def parse_tarot_json(tarot_cards_json):
    """
    解析塔羅牌結果的 JSON 字串。

    Args:
        tarot_cards_json (str): JSON 字串

    Returns:
        list[dict]: 解析後的牌列表，每個元素包含 card_id、position、is_reversed
    """
    if not tarot_cards_json:
        return []
    try:
        return json.loads(tarot_cards_json)
    except (json.JSONDecodeError, TypeError):
        return []
