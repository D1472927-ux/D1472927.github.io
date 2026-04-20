"""
draw.py — 抽籤（求籤）路由

Blueprint: draw_bp
URL Prefix: /draw

路由：
- GET  /draw             — 抽籤頁面（選類別、輸入問題）
- POST /draw             — 抽籤處理（隨機抽籤、儲存結果）
- GET  /draw/result/<id> — 籤詩結果頁
"""

from flask import Blueprint, render_template, request, redirect, url_for, session

draw_bp = Blueprint('draw', __name__, url_prefix='/draw')


@draw_bp.route('/', methods=['GET'])
def index():
    """
    抽籤頁面

    處理邏輯：
    1. 呼叫 poem.get_categories() 取得可用類別
    渲染 draw/index.html，傳遞 categories 清單
    """
    # TODO: 取得籤詩類別清單
    # TODO: 渲染 draw/index.html
    pass


@draw_bp.route('/', methods=['POST'])
def draw():
    """
    抽籤處理

    表單欄位：category（必填）, question（選填）
    處理邏輯：
    1. 呼叫 poem.get_random(category) 隨機取得籤詩
    2. 組合 result_summary（如「上籤 — 龍飛九天」）
    3. 呼叫 fortune.create(type='draw', ...) 儲存結果
       - user_id 從 session 取得，未登入時為 None
    重導向至 /draw/result/<fortune_id>
    """
    # TODO: 取得表單資料
    # TODO: 呼叫 Model 隨機抽籤
    # TODO: 儲存結果
    # TODO: 重導向至結果頁
    pass


@draw_bp.route('/result/<int:id>')
def result(id):
    """
    籤詩結果頁

    URL 參數：id（fortune ID）
    處理邏輯：
    1. 呼叫 fortune.get_by_id(id) 取得結果（含 JOIN 籤詩資料）
    渲染 draw/result.html
    404：紀錄不存在
    """
    # TODO: 呼叫 Model 取得結果
    # TODO: 渲染 draw/result.html 或回傳 404
    pass
