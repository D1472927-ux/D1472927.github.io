"""
draw.py — 抽籤（求籤）路由

Blueprint: draw_bp
URL Prefix: /draw

路由：
- GET  /draw             — 抽籤頁面（選類別、輸入問題）
- POST /draw             — 抽籤處理（隨機抽籤、儲存結果）
- GET  /draw/result/<id> — 籤詩結果頁
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import poem, fortune

draw_bp = Blueprint('draw', __name__, url_prefix='/draw')


@draw_bp.route('/', methods=['GET'])
def index():
    """
    抽籤頁面

    顯示類別選擇與問題輸入表單。
    """
    categories = poem.get_categories()

    # 若還沒有種子資料，給預設類別
    if not categories:
        categories = ['事業', '感情', '學業', '健康', '財運']

    return render_template('draw/index.html', categories=categories)


@draw_bp.route('/', methods=['POST'])
def draw():
    """
    抽籤處理

    1. 取得使用者選擇的類別與問題
    2. 隨機抽取一支籤詩
    3. 儲存結果至 fortunes 表
    4. 重導向至結果頁
    """
    category = request.form.get('category', '').strip()
    question = request.form.get('question', '').strip() or None

    if not category:
        flash('請選擇一個類別', 'warning')
        return redirect(url_for('draw.index'))

    # 隨機抽籤
    drawn_poem = poem.get_random(category)
    if not drawn_poem:
        flash('目前沒有籤詩資料，請稍後再試', 'danger')
        return redirect(url_for('draw.index'))

    # 組合結果摘要
    result_summary = f'{drawn_poem["level"]} — {drawn_poem["title"]}'

    # 取得使用者 ID（未登入時為 None）
    user_id = session.get('user_id')

    # 儲存結果
    fortune_id = fortune.create(
        type='draw',
        category=category,
        question=question,
        poem_id=drawn_poem['id'],
        result_summary=result_summary,
        user_id=user_id
    )

    if fortune_id:
        return redirect(url_for('draw.result', id=fortune_id))
    else:
        flash('儲存結果失敗，請稍後再試', 'danger')
        return redirect(url_for('draw.index'))


@draw_bp.route('/result/<int:id>')
def result(id):
    """
    籤詩結果頁

    顯示籤詩等級、籤題、原文、白話文解釋。
    """
    fortune_data = fortune.get_by_id(id)
    if not fortune_data:
        abort(404)

    return render_template('draw/result.html', fortune=fortune_data)
