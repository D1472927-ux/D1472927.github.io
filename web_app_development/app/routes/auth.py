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
from app.models import user
from app.routes.utils import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET'])
def register_page():
    """
    註冊頁面

    若已登入則重導向至首頁。
    """
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/register.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    註冊處理

    表單欄位：username, password, password_confirm
    驗證：欄位非空、密碼一致、帳號不重複
    """
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    password_confirm = request.form.get('password_confirm', '')

    # 驗證欄位非空
    if not username or not password:
        flash('請填寫帳號和密碼', 'danger')
        return render_template('auth/register.html')

    # 驗證密碼一致
    if password != password_confirm:
        flash('兩次密碼輸入不一致', 'danger')
        return render_template('auth/register.html')

    # 檢查帳號是否已存在
    existing = user.get_by_username(username)
    if existing:
        flash('此帳號已被使用，請選擇其他帳號', 'danger')
        return render_template('auth/register.html')

    # 建立使用者
    new_id = user.create(username, password)
    if new_id:
        flash('註冊成功，請登入', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('註冊失敗，請稍後再試', 'danger')
        return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET'])
def login_page():
    """
    登入頁面

    若已登入則重導向至首頁。
    """
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    登入處理

    表單欄位：username, password
    驗證通過 → 設定 session，重導向至首頁
    """
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')

    if not username or not password:
        flash('請填寫帳號和密碼', 'danger')
        return render_template('auth/login.html')

    # 驗證帳號密碼
    verified_user = user.verify_password(username, password)
    if verified_user:
        session['user_id'] = verified_user['id']
        session['username'] = verified_user['username']
        flash(f'歡迎回來，{verified_user["username"]}！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('帳號或密碼錯誤', 'danger')
        return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """
    登出

    清除 session，重導向至首頁。
    """
    session.clear()
    flash('已成功登出', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """
    個人中心（需登入）

    顯示個人資訊與統計數據（算命次數、捐獻總額）。
    """
    user_data = user.get_by_id(session['user_id'])
    stats = user.get_stats(session['user_id'])
    return render_template('profile/index.html', user=user_data, stats=stats)
