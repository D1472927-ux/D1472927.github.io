"""
utils.py — 共用工具函式

提供路由層使用的通用工具，如登入驗證裝飾器。
"""

from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    登入保護裝飾器。

    用於需要登入才能存取的路由。
    若使用者未登入，會重導向至登入頁面並顯示提示訊息。

    使用方式：
        @app.route('/protected')
        @login_required
        def protected_page():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('請先登入', 'warning')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function
