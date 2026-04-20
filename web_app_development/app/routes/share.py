"""
share.py — 分享功能路由

Blueprint: share_bp
URL Prefix: /share

路由：
- GET /share/<token> — 分享結果頁（公開頁面，不需登入）
"""

from flask import Blueprint, render_template, abort

share_bp = Blueprint('share', __name__, url_prefix='/share')


@share_bp.route('/<token>')
def result(token):
    """
    分享結果頁（公開）

    URL 參數：token（share_token，UUID 格式）
    處理邏輯：
    1. 呼叫 fortune.get_by_share_token(token) 取得結果
    2. 若為抽籤類型 → 顯示籤詩卡片
    3. 若為塔羅類型 → 解析 JSON，取得牌資料，顯示牌陣卡片
    渲染 share/result.html（以美觀的卡片格式呈現）
    404：token 不存在
    """
    # TODO: 呼叫 Model 取得結果
    # TODO: 根據類型處理資料
    # TODO: 渲染 share/result.html 或回傳 404
    pass
