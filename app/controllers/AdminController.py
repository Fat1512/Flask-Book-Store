import app.utils.admin
from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import get_books_by_gerne, total_revenue_per_gerne, book_statistic_frequency
from datetime import datetime
import math
from app import app, db
from app.model.BookGerne import BookGerne

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
def admin_statistic_revenue():
    kw = request.args.get('kw')
    # from_date = request.args.get('from_date')
    # to_date = request.args.get('to_date')
    selected_month = request.args.get('selected_month')
    stats = book_gerne_statistic(kw=kw, selected_month=selected_month)
    page = int(request.args.get('page', 1))  # Lấy số trang hiện tại từ URL, mặc định là 1
    page_size = app.config['STATISTIC_REVEN_PAGE_SIZE']  # Kích thước mỗi trang
    total = len(stats)  # Tổng số bản ghi
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]  # Lấy dữ liệu theo trang
    total_revenue = total_revenue_per_gerne(kw=kw, selected_month=selected_month)
    return render_template(
        "admin-statistic-revenue.html",
        stats=paginated_stats,  # Dữ liệu đã phân trang
        total_revenue=total_revenue,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1)
        }
    )


@admin_bp.route("/statistic-frequency")
@admin_required
def admin_statistic_frequency():
    gerne_id = request.args.get('gerne_id', type=int)

    if gerne_id == 1:
        stats = book_statistic_frequency()
    else:
        stats = book_statistic_frequency(gerne_id)

    page = int(request.args.get('page', 1))
    page_size = app.config['STATISTIC_FRE_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    # Render template
    return render_template(
        "admin-statistic-frequency.html",
        stats=paginated_stats,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )


@admin_bp.route("/statistic")
@admin_required
def admin_statistic():
    return render_template("admin-statistic.html")


@admin_bp.route("/api/gernes", methods=["GET"])
@admin_required
def get_gernes():
    gernes = db.session.query(BookGerne.book_gerne_id, BookGerne.name).all()
    return jsonify([{"id": gerne.book_gerne_id, "name": gerne.name} for gerne in gernes])

#
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


