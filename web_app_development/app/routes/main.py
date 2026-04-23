"""
main.py — 首頁與每日運勢路由

Blueprint: main_bp
URL Prefix: 無

路由：
- GET /        — 首頁
- GET /fortune — 每日運勢頁
"""

import hashlib
from datetime import date
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


def _generate_daily_fortune():
    """
    根據今天日期產生每日運勢資料。

    使用日期字串的雜湊值作為種子，確保同一天的運勢固定不變。

    Returns:
        dict: 包含各面向運勢（1~5 星）、幸運色、幸運數字
    """
    today = date.today().isoformat()  # 如 '2026-04-20'

    # 用日期的雜湊值產生固定的「隨機」數值
    hash_bytes = hashlib.md5(today.encode()).hexdigest()

    # 將 hash 的不同部分映射到 1~5 的星數
    overall = int(hash_bytes[0], 16) % 5 + 1
    love = int(hash_bytes[2], 16) % 5 + 1
    career = int(hash_bytes[4], 16) % 5 + 1
    money = int(hash_bytes[6], 16) % 5 + 1

    # 幸運色
    colors = ['紅色', '橙色', '金色', '綠色', '藍色', '紫色', '白色', '粉紅色']
    lucky_color = colors[int(hash_bytes[8], 16) % len(colors)]

    # 幸運數字（1~99）
    lucky_number = int(hash_bytes[10:12], 16) % 99 + 1

    return {
        'date': today,
        'overall': overall,
        'love': love,
        'career': career,
        'money': money,
        'lucky_color': lucky_color,
        'lucky_number': lucky_number
    }


@main_bp.route('/')
def index():
    """
    首頁

    - 顯示系統入口與功能選單
    - 展示今日運勢摘要
    """
    daily_summary = _generate_daily_fortune()
    return render_template('index.html', daily_summary=daily_summary)


@main_bp.route('/fortune')
def daily_fortune():
    """
    每日運勢頁

    - 顯示完整的今日運勢（整體/愛情/事業/財運，1~5 星）
    - 幸運色與幸運數字
    """
    fortune = _generate_daily_fortune()
    return render_template('fortune/daily.html', fortune=fortune)
