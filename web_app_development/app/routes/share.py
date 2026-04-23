"""
share.py — 分享功能路由

Blueprint: share_bp
URL Prefix: /share

路由：
- GET /share/<token> — 分享結果頁（公開頁面，不需登入）
"""

from flask import Blueprint, render_template, abort
from app.models import fortune, tarot

share_bp = Blueprint('share', __name__, url_prefix='/share')


@share_bp.route('/<token>')
def result(token):
    """
    分享結果頁（公開）

    根據 share_token 取得算命結果，以卡片格式呈現。
    支援抽籤結果與塔羅占卜結果的展示。
    """
    fortune_data = fortune.get_by_share_token(token)
    if not fortune_data:
        abort(404)

    # 若為塔羅類型，解析 JSON 取得牌資料
    cards = []
    if fortune_data['type'] == 'tarot':
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

    return render_template('share/result.html', fortune=fortune_data, cards=cards)
