"""
donate.py — 捐獻香油錢路由

Blueprint: donate_bp
URL Prefix: /donate

路由：
- GET  /donate             — 捐獻頁面
- POST /donate             — 捐獻處理
- GET  /donate/thanks/<id> — 感謝頁面
- GET  /donate/history     — 捐獻紀錄

所有路由皆需登入。
注意：MVP 階段僅模擬捐獻流程，不串接真實金流。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

donate_bp = Blueprint('donate', __name__, url_prefix='/donate')


@donate_bp.route('/', methods=['GET'])
def index():
    """
    捐獻頁面（需登入）

    渲染 donate/index.html，顯示：
    - 預設金額選項（100 / 300 / 500 / 1000）
    - 自訂金額輸入
    - 祈願內容（選填）
    - 具名/匿名選擇
    未登入 → 重導向至 /login
    """
    # TODO: 檢查登入狀態
    # TODO: 渲染 donate/index.html
    pass


@donate_bp.route('/', methods=['POST'])
def donate():
    """
    捐獻處理（需登入）

    表單欄位：
    - amount（必填，預設金額選項）
    - custom_amount（選填，自訂金額）
    - wish（選填，文字）
    - is_anonymous（選填，checkbox）

    處理邏輯：
    1. 決定最終金額（預設或自訂）
    2. 驗證金額為正整數
    3. 呼叫 donation.create(user_id, amount, wish, is_anonymous) 儲存
    重導向至 /donate/thanks/<donation_id>
    驗證失敗 → 重新渲染表單
    """
    # TODO: 取得表單資料
    # TODO: 驗證金額
    # TODO: 呼叫 Model 儲存
    # TODO: 重導向至感謝頁
    pass


@donate_bp.route('/thanks/<int:id>')
def thanks(id):
    """
    捐獻感謝頁（需登入）

    URL 參數：id（donation ID）
    處理邏輯：
    1. 呼叫 donation.get_by_id(id) 取得捐獻資料
    渲染 donate/thanks.html
    404：紀錄不存在
    """
    # TODO: 呼叫 Model 取得資料
    # TODO: 渲染 donate/thanks.html 或回傳 404
    pass


@donate_bp.route('/history')
def history():
    """
    捐獻紀錄（需登入）

    處理邏輯：
    1. 呼叫 donation.get_by_user(user_id) 取得紀錄
    2. 呼叫 donation.get_user_total(user_id) 取得總額
    渲染 donate/history.html，傳遞 records 與 total
    未登入 → 重導向至 /login
    """
    # TODO: 檢查登入狀態
    # TODO: 呼叫 Model 取得紀錄與總額
    # TODO: 渲染 donate/history.html
    pass
