"""
app/__init__.py — Flask 應用程式工廠函式

使用 Application Factory 模式建立 Flask 應用程式。
負責：
1. 建立 Flask app 實例
2. 載入設定
3. 註冊所有 Blueprint
4. 初始化資料庫
"""

from flask import Flask
from config import Config


def create_app():
    """
    Flask 應用程式工廠函式。

    Returns:
        Flask: 已設定好的 Flask 應用程式實例
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # --------------------------------------------------
    # 註冊 Blueprint（路由模組）
    # --------------------------------------------------
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.draw import draw_bp
    from app.routes.tarot import tarot_bp
    from app.routes.history import history_bp
    from app.routes.donate import donate_bp
    from app.routes.share import share_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(draw_bp)       # url_prefix: /draw
    app.register_blueprint(tarot_bp)      # url_prefix: /tarot
    app.register_blueprint(history_bp)    # url_prefix: /history
    app.register_blueprint(donate_bp)     # url_prefix: /donate
    app.register_blueprint(share_bp)      # url_prefix: /share

    # --------------------------------------------------
    # 初始化資料庫（首次啟動時自動建表與匯入種子資料）
    # --------------------------------------------------
    with app.app_context():
        from app.models.db import init_db, seed_db
        init_db()
        seed_db()

    return app
