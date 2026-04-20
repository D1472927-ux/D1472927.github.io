"""
auth.py — 使用者帳號路由（註冊、登入、登出、個人中心）

Blueprint: auth_bp
URL Prefix: 無

路由：
- GET  /register — 註冊頁面
- POST /register — 註冊處理
- GET  /login    — 登入頁面
- POST /login    — 登入處理
- GET  /logout   — 登出
- GET  /profile  — 個人中心
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """
    註冊頁面

    - 若已登入則重導向至首頁
    - 渲染 auth/register.html
    """
    # TODO: 檢查是否已登入
    # TODO: 渲染 auth/register.html
    pass


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    註冊處理

    表單欄位：username, password, password_confirm
    處理邏輯：
    1. 驗證欄位非空
    2. 驗證密碼一致
    3. 呼叫 user.get_by_username() 檢查帳號是否已存在
    4. 呼叫 user.create() 建立使用者
    成功 → 重導向至 /login
    失敗 → 重新渲染表單，顯示錯誤
    """
    # TODO: 取得表單資料
    # TODO: 驗證欄位
    # TODO: 呼叫 Model 建立使用者
    # TODO: 重導向至登入頁
    pass


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """
    登入頁面

    - 若已登入則重導向至首頁
    - 渲染 auth/login.html
    """
    # TODO: 檢查是否已登入
    # TODO: 渲染 auth/login.html
    pass


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    登入處理

    表單欄位：username, password
    處理邏輯：
    1. 呼叫 user.verify_password() 驗證
    2. 成功 → 設定 session['user_id'] 與 session['username']
    3. 重導向至首頁
    失敗 → 重新渲染登入頁，顯示錯誤
    """
    # TODO: 取得表單資料
    # TODO: 呼叫 Model 驗證
    # TODO: 設定 Session
    # TODO: 重導向
    pass


@auth_bp.route('/logout')
def logout():
    """
    登出

    - 清除 session（session.clear()）
    - 重導向至首頁
    """
    # TODO: 清除 session
    # TODO: 重導向至首頁
    pass


@auth_bp.route('/profile')
def profile():
    """
    個人中心（需登入）

    處理邏輯：
    1. 呼叫 user.get_by_id(user_id) 取得個人資訊
    2. 呼叫 user.get_stats(user_id) 取得統計（算命次數、捐獻總額）
    渲染 profile/index.html
    """
    # TODO: 檢查登入狀態
    # TODO: 呼叫 Model 取得資料
    # TODO: 渲染 profile/index.html
    pass
