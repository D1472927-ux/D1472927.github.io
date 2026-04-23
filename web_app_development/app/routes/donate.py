"""
donate.py — 捐獻香油錢路由

Blueprint: donate_bp
URL Prefix: /donate

路由：
- GET  /donate             — 捐獻頁面
- POST /donate             — 捐獻處理
- GET  /donate/thanks/<id> — 感謝頁面
- GET  /donate/history     — 捐獻紀錄

所有路由皆需登入。
注意：MVP 階段僅模擬捐獻流程，不串接真實金流。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models import donation
from app.routes.utils import login_required

donate_bp = Blueprint('donate', __name__, url_prefix='/donate')

# 預設捐獻金額選項
DEFAULT_AMOUNTS = [100, 300, 500, 1000]


@donate_bp.route('/', methods=['GET'])
@login_required
def index():
    """
    捐獻頁面（需登入）

    顯示金額選擇、祈願輸入、匿名選項。
    """
    return render_template('donate/index.html', default_amounts=DEFAULT_AMOUNTS)


@donate_bp.route('/', methods=['POST'])
@login_required
def donate():
    """
    捐獻處理（需登入）

    驗證金額後記錄捐獻。
    """
    user_id = session['user_id']

    # 取得金額（優先使用自訂金額）
    custom_amount = request.form.get('custom_amount', '').strip()
    preset_amount = request.form.get('amount', '').strip()

    if custom_amount:
        amount_str = custom_amount
    elif preset_amount:
        amount_str = preset_amount
    else:
        flash('請選擇或輸入捐獻金額', 'warning')
        return render_template('donate/index.html', default_amounts=DEFAULT_AMOUNTS)

    # 驗證金額為正整數
    try:
        amount = int(amount_str)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        flash('請輸入有效的金額（正整數）', 'danger')
        return render_template('donate/index.html', default_amounts=DEFAULT_AMOUNTS)

    # 取得其他欄位
    wish = request.form.get('wish', '').strip() or None
    is_anonymous = 1 if request.form.get('is_anonymous') else 0

    # 儲存捐獻紀錄
    donation_id = donation.create(user_id, amount, wish, is_anonymous)
    if donation_id:
        flash('感謝您的捐獻！🙏', 'success')
        return redirect(url_for('donate.thanks', id=donation_id))
    else:
        flash('捐獻處理失敗，請稍後再試', 'danger')
        return render_template('donate/index.html', default_amounts=DEFAULT_AMOUNTS)


@donate_bp.route('/thanks/<int:id>')
@login_required
def thanks(id):
    """
    捐獻感謝頁（需登入）

    顯示感謝訊息與捐獻摘要。
    """
    donation_data = donation.get_by_id(id)
    if not donation_data:
        abort(404)

    return render_template('donate/thanks.html', donation=donation_data)


@donate_bp.route('/history')
@login_required
def history():
    """
    捐獻紀錄（需登入）

    顯示個人捐獻紀錄與總額。
    """
    user_id = session['user_id']
    records = donation.get_by_user(user_id)
    total = donation.get_user_total(user_id)
    return render_template('donate/history.html', records=records, total=total)
