"""
main.py — 首頁與每日運勢路由

Blueprint: main_bp
URL Prefix: 無

路由：
- GET /        — 首頁
- GET /fortune — 每日運勢頁
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    首頁

    - 顯示系統入口與功能選單
    - 展示今日運勢摘要
    - 呼叫每日運勢產生邏輯，傳遞 daily_summary 給模板
    """
    # TODO: 產生今日運勢摘要
    # TODO: 渲染 index.html
    pass


@main_bp.route('/fortune')
def daily_fortune():
    """
    每日運勢頁

    - 以今天日期為種子，產生各面向運勢（整體/愛情/事業/財運，1~5 星）
    - 產生幸運色與幸運數字
    - 渲染 fortune/daily.html
    """
    # TODO: 根據日期產生運勢資料
    # TODO: 渲染 fortune/daily.html
    pass
