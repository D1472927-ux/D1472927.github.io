"""
history.py — 歷史紀錄路由

Blueprint: history_bp
URL Prefix: /history

路由：
- GET  /history             — 歷史紀錄列表（支援篩選）
- POST /history/delete/<id> — 刪除紀錄

所有路由皆需登入。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import fortune
from app.routes.utils import login_required

history_bp = Blueprint('history', __name__, url_prefix='/history')


@history_bp.route('/')
@login_required
def index():
    """
    歷史紀錄列表（需登入）

    支援依類型（draw/tarot）和日期篩選。
    """
    user_id = session['user_id']

    # 取得篩選參數
    type_filter = request.args.get('type', '').strip() or None
    date_from = request.args.get('date', '').strip() or None

    # 驗證篩選參數
    if type_filter and type_filter not in ('draw', 'tarot'):
        type_filter = None

    # 查詢紀錄
    records = fortune.get_by_user(user_id, type_filter=type_filter, date_from=date_from)

    return render_template('history/index.html',
                           records=records,
                           type_filter=type_filter,
                           date_from=date_from)


@history_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """
    刪除紀錄（需登入）

    驗證該紀錄屬於當前使用者後才允許刪除。
    """
    user_id = session['user_id']

    # 取得紀錄並驗證擁有者
    record = fortune.get_by_id(id)
    if not record:
        abort(404)

    if record['user_id'] != user_id:
        flash('您無權刪除此紀錄', 'danger')
        return redirect(url_for('history.index'))

    # 刪除紀錄
    if fortune.delete(id):
        flash('紀錄已刪除', 'success')
    else:
        flash('刪除失敗，請稍後再試', 'danger')

    return redirect(url_for('history.index'))
