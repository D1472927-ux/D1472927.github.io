"""
tarot.py — 塔羅占卜路由

Blueprint: tarot_bp
URL Prefix: /tarot

路由：
- GET  /tarot             — 塔羅占卜頁面（選主題、選牌陣）
- POST /tarot             — 塔羅占卜處理（隨機翻牌、儲存結果）
- GET  /tarot/result/<id> — 塔羅結果頁
"""

import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import tarot, fortune

tarot_bp = Blueprint('tarot', __name__, url_prefix='/tarot')

# 占卜主題與對應的牌陣類型
TOPICS = {
    '今日運勢': {'spread': 'single', 'count': 1, 'positions': ['啟示']},
    '感情問題': {'spread': 'three', 'count': 3, 'positions': ['過去', '現在', '未來']},
    '工作抉擇': {'spread': 'three', 'count': 3, 'positions': ['現狀', '挑戰', '建議']}
}


@tarot_bp.route('/', methods=['GET'])
def index():
    """
    塔羅占卜頁面

    顯示主題選擇（今日運勢、感情問題、工作抉擇）。
    """
    topics = list(TOPICS.keys())
    return render_template('tarot/index.html', topics=topics)


@tarot_bp.route('/', methods=['POST'])
def divine():
    """
    塔羅占卜處理

    1. 取得使用者選擇的主題
    2. 根據主題決定抽牌數量
    3. 隨機翻牌（含正/逆位）
    4. 將結果序列化為 JSON 並儲存
    5. 重導向至結果頁
    """
    topic = request.form.get('topic', '').strip()

    if topic not in TOPICS:
        flash('請選擇一個占卜主題', 'warning')
        return redirect(url_for('tarot.index'))

    topic_config = TOPICS[topic]
    count = topic_config['count']
    positions = topic_config['positions']

    # 隨機抽牌
    drawn_cards = tarot.draw_cards(count)
    if not drawn_cards:
        flash('目前沒有塔羅牌資料，請稍後再試', 'danger')
        return redirect(url_for('tarot.index'))

    # 序列化為 JSON（儲存到資料庫）
    tarot_json_data = []
    for i, drawn in enumerate(drawn_cards):
        tarot_json_data.append({
            'card_id': drawn['card']['id'],
            'position': positions[i] if i < len(positions) else f'牌{i+1}',
            'is_reversed': drawn['is_reversed']
        })

    tarot_cards_json = json.dumps(tarot_json_data, ensure_ascii=False)

    # 組合結果摘要
    card_names = [d['card']['name'] for d in drawn_cards]
    result_summary = f'塔羅占卜 — {topic}：{", ".join(card_names)}'

    # 取得使用者 ID
    user_id = session.get('user_id')

    # 儲存結果
    fortune_id = fortune.create(
        type='tarot',
        category=topic,
        tarot_cards_json=tarot_cards_json,
        result_summary=result_summary,
        user_id=user_id
    )

    if fortune_id:
        return redirect(url_for('tarot.result', id=fortune_id))
    else:
        flash('儲存結果失敗，請稍後再試', 'danger')
        return redirect(url_for('tarot.index'))


@tarot_bp.route('/result/<int:id>')
def result(id):
    """
    塔羅結果頁

    解析 JSON 取得每張牌的完整資料，並顯示牌義解讀。
    """
    fortune_data = fortune.get_by_id(id)
    if not fortune_data:
        abort(404)

    # 解析塔羅 JSON，取得每張牌的完整資料
    cards = []
    tarot_json = fortune.parse_tarot_json(fortune_data.get('tarot_cards_json'))
    for item in tarot_json:
        card_data = tarot.get_by_id(item['card_id'])
        if card_data:
            is_reversed = item.get('is_reversed', False)
            cards.append({
                'card': card_data,
                'position': item.get('position', ''),
                'is_reversed': is_reversed,
                'meaning': card_data['reversed_meaning'] if is_reversed else card_data['upright_meaning'],
                'description': card_data['reversed_description'] if is_reversed else card_data['upright_description']
            })

    return render_template('tarot/result.html', fortune=fortune_data, cards=cards)
