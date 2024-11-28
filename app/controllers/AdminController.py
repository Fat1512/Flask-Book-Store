from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import get_books_by_gerne, total_revenue_per_gerne
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.admin_login'))
        if current_user.user_role != UserRole.ADMIN:
            return redirect(url_for('account.admin_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@admin_bp.route("/")
@admin_required
def admin_home():
    return render_template("admin-home.html")


@admin_bp.route("/add-products")
def add_products_process():
    return render_template("employee-add-products.html")


@admin_bp.route("/statistic-revenue")
@admin_required
def admin_statistic():
    kw = request.args.get('kw')
    # from_date = request.args.get('from_date')
    # to_date = request.args.get('to_date')
    selected_month = request.args.get('selected_month')
    stats = book_gerne_statistic(kw=kw,selected_month=selected_month)
    total_revenue = total_revenue_per_gerne(kw=kw, selected_month=selected_month)
    return render_template("admin-statistic-revenue.html", stats=stats, total_revenue=total_revenue)

# @admin_bp.route('/api/gernes', methods=['GET'])
# def get_gernes():
#     gernes = book_gerne_statistic()
#     return jsonify([{"id": gerne[0], "name": gerne[1]} for gerne in gernes])



# @admin_bp.route('/admin/api/gerne-stats', methods=['GET'])
# def gerne_stats():
#     gerne_id = request.args.get('gerne_id', type=int)
#     if gerne_id == 1:  # Nếu là thể loại tất cả
#         stats = book_gerne_statistic()
#         return jsonify([{
#             "id": s[0],
#             "name": s[1],
#             "count": s[2]
#         } for s in stats])
#     else:  # Lấy theo thể loại cụ thể
#         books = get_books_by_gerne(gerne_id)
#         return jsonify([{
#             "id": b[0],
#             "title": b[1],
#             "quantity": b[2]
#         } for b in books])


