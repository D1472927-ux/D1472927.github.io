"""
history.py — 歷史紀錄路由

Blueprint: history_bp
URL Prefix: /history

路由：
- GET  /history             — 歷史紀錄列表（支援篩選）
- POST /history/delete/<id> — 刪除紀錄

所有路由皆需登入。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

history_bp = Blueprint('history', __name__, url_prefix='/history')


@history_bp.route('/')
def index():
    """
    歷史紀錄列表（需登入）

    Query 參數：
    - type（選填）：篩選類型（draw / tarot）
    - date（選填）：篩選起始日期（ISO 格式）

    處理邏輯：
    1. 從 session 取得 user_id
    2. 呼叫 fortune.get_by_user(user_id, type_filter, date_from) 取得紀錄
    渲染 history/index.html，傳遞 records 與篩選條件
    未登入 → 重導向至 /login
    """
    # TODO: 檢查登入狀態
    # TODO: 取得篩選參數
    # TODO: 呼叫 Model 取得紀錄
    # TODO: 渲染 history/index.html
    pass


@history_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """
    刪除紀錄（需登入）

    URL 參數：id（fortune ID）
    處理邏輯：
    1. 驗證該紀錄屬於當前使用者
    2. 呼叫 fortune.delete(id) 刪除
    重導向至 /history，顯示 flash 訊息
    403：非本人紀錄
    404：紀錄不存在
    """
    # TODO: 檢查登入狀態
    # TODO: 驗證紀錄擁有者
    # TODO: 呼叫 Model 刪除
    # TODO: 重導向至歷史紀錄頁
    pass
