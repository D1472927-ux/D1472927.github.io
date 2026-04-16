"""
tarot.py — 塔羅牌資料模型

對應資料表：tarot_cards
功能：塔羅牌的查詢與管理，核心方法為隨機抽牌

塔羅牌屬於靜態參考資料（22 張大阿爾克那），
主要透過 seed.sql 匯入。
"""

import random
from app.models.db import get_connection


def create(name, upright_meaning, reversed_meaning,
           upright_description, reversed_description, image_url=None):
    """
    新增一張塔羅牌。

    Args:
        name (str): 塔羅牌名稱（如「愚者 The Fool」）
        upright_meaning (str): 正位關鍵字
        reversed_meaning (str): 逆位關鍵字
        upright_description (str): 正位詳細解讀
        reversed_description (str): 逆位詳細解讀
        image_url (str, optional): 牌面圖片路徑

    Returns:
        int: 新建立的塔羅牌 ID
    """
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
    finally:
        conn.close()


def get_all():
    """
    取得所有塔羅牌。

    Returns:
        list[dict]: 所有塔羅牌清單
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            'SELECT * FROM tarot_cards ORDER BY id'
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_by_id(card_id):
    """
    依 ID 取得特定塔羅牌。

    Args:
        card_id (int): 塔羅牌 ID

    Returns:
        dict or None: 塔羅牌資料，若不存在回傳 None
    """
    conn = get_connection()
    try:
        row = conn.execute(
            'SELECT * FROM tarot_cards WHERE id = ?', (card_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def draw_cards(count=1):
    """
    隨機抽取指定數量的塔羅牌，並決定正位/逆位。

    此為塔羅占卜的核心邏輯：
    1. 從所有塔羅牌中隨機抽取 count 張（不重複）
    2. 每張牌隨機決定正位或逆位（50% 機率）

    Args:
        count (int): 要抽取的牌數（1 = 單牌，3 = 三牌占卜）

    Returns:
        list[dict]: 抽到的牌列表，每個元素包含：
            - card: 塔羅牌完整資料
            - is_reversed: 是否逆位 (bool)
            - meaning: 對應方向的關鍵字
            - description: 對應方向的詳細解讀
    """
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
    finally:
        conn.close()


def update(card_id, name=None, image_url=None, upright_meaning=None,
           reversed_meaning=None, upright_description=None,
           reversed_description=None):
    """
    更新塔羅牌資料。

    Args:
        card_id (int): 塔羅牌 ID
        name (str, optional): 新名稱
        image_url (str, optional): 新圖片路徑
        upright_meaning (str, optional): 新正位關鍵字
        reversed_meaning (str, optional): 新逆位關鍵字
        upright_description (str, optional): 新正位解讀
        reversed_description (str, optional): 新逆位解讀

    Returns:
        bool: 是否更新成功
    """
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
    finally:
        conn.close()


def delete(card_id):
    """
    刪除塔羅牌。

    Args:
        card_id (int): 塔羅牌 ID

    Returns:
        bool: 是否刪除成功
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            'DELETE FROM tarot_cards WHERE id = ?', (card_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
