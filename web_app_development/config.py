"""
config.py — Flask 應用程式設定檔

包含資料庫路徑、密鑰等設定。
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Flask 設定類別"""

    # Flask 密鑰（用於 Session 加密與 CSRF 保護）
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')

    # SQLite 資料庫路徑
    DATABASE = os.path.join(BASE_DIR, 'instance', 'database.db')

    # 是否開啟 Debug 模式
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
