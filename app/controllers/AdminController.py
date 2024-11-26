from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import get_books_by_genre

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


@admin_bp.route("/statistic")
def admin_statistic():
    stats = book_gerne_statistic()
    return render_template("admin-statistic.html", stats=stats)

@admin_bp.route('/api/genres', methods=['GET'])
def get_genres():
    genres = book_gerne_statistic()
    return jsonify([{"id": genre[0], "name": genre[1]} for genre in genres])

# @admin_bp.route('/admin/api/genre-stats', methods=['GET'])
# def genre_stats():
#     genre_id = request.args.get('genre_id', type=int)
#     if genre_id == 1:  # Nếu là thể loại tất cả
#         stats = book_gerne_statistic()
#         return jsonify([{
#             "id": s[0],
#             "name": s[1],
#             "count": s[2]
#         } for s in stats])
#     else:  # Lấy theo thể loại cụ thể
#         books = get_books_by_genre(genre_id)
#         return jsonify([{
#             "id": b[0],
#             "title": b[1],
#             "quantity": b[2]
#         } for b in books])


