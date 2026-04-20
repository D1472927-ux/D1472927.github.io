"""
tarot.py — 塔羅占卜路由

Blueprint: tarot_bp
URL Prefix: /tarot

路由：
- GET  /tarot             — 塔羅占卜頁面（選主題、選牌陣）
- POST /tarot             — 塔羅占卜處理（隨機翻牌、儲存結果）
- GET  /tarot/result/<id> — 塔羅結果頁
"""

from flask import Blueprint, render_template, request, redirect, url_for, session

tarot_bp = Blueprint('tarot', __name__, url_prefix='/tarot')


@tarot_bp.route('/', methods=['GET'])
def index():
    """
    塔羅占卜頁面

    渲染 tarot/index.html，傳遞主題清單：
    - 今日運勢（單牌占卜）
    - 感情問題（三牌占卜）
    - 工作抉擇（三牌占卜）
    """
    # TODO: 渲染 tarot/index.html
    pass


@tarot_bp.route('/', methods=['POST'])
def divine():
    """
    塔羅占卜處理

    表單欄位：topic（必填）, spread（必填：single / three）
    處理邏輯：
    1. 根據 spread 決定抽牌數量（1 或 3）
    2. 呼叫 tarot.draw_cards(count) 隨機抽牌（含正/逆位）
    3. 將結果序列化為 JSON
    4. 呼叫 fortune.create(type='tarot', category=topic, tarot_cards_json=...) 儲存
    重導向至 /tarot/result/<fortune_id>
    """
    # TODO: 取得表單資料
    # TODO: 呼叫 Model 隨機抽牌
    # TODO: 序列化為 JSON 並儲存
    # TODO: 重導向至結果頁
    pass


@tarot_bp.route('/result/<int:id>')
def result(id):
    """
    塔羅結果頁

    URL 參數：id（fortune ID）
    處理邏輯：
    1. 呼叫 fortune.get_by_id(id) 取得結果
    2. 呼叫 fortune.parse_tarot_json() 解析塔羅 JSON
    3. 對每張牌呼叫 tarot.get_by_id() 取得完整牌資料
    渲染 tarot/result.html
    404：紀錄不存在
    """
    # TODO: 呼叫 Model 取得結果
    # TODO: 解析塔羅牌 JSON
    # TODO: 渲染 tarot/result.html 或回傳 404
    pass
