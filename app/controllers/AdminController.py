import app.utils.admin
from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import total_revenue_per_gerne, book_statistic_frequency, account_management, book_management
from datetime import datetime
import math
from app import app, db
from app.model.BookGerne import BookGerne
from app.model.User import User
from app.model.Book import Book
from app.model.Account import Account
from app.model.Publisher import Publisher

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


@admin_bp.route("/book-manager")
@admin_required
def admin_book_manager():
    gerne_id = request.args.get('gerne_id', type=int)

    if gerne_id == 1:
        stats = book_management()
    else:
        stats = book_management(gerne_id)

    page = int(request.args.get('page', 1))
    page_size = app.config['BOOK_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    # Render template
    return render_template(
        "admin-book-manager.html",
        stats=paginated_stats, full_stats=stats,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )


@admin_bp.route("/statistic-revenue")
@admin_required
def admin_statistic_revenue():
    kw = request.args.get('kw')
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
        stats=paginated_stats,
        full_stats=stats,
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
        stats=paginated_stats, full_stats=stats,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )


@admin_bp.route("/account-manager")
@admin_required
def admin_account_manager():
    user_role = request.args.get('user_role', type=int)
    stats = account_management(user_role)

    # Kiểm tra có dữ liệu không
    print(stats)

    page = int(request.args.get('page', 1))
    page_size = app.config['STATISTIC_FRE_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    return render_template(
        "admin-account-manager.html",
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

@admin_bp.route("/api/user_roles", methods=["GET"])
@admin_required
def get_user_roles():
    try:
        user_roles = db.session.query(User.user_role).distinct().all()

        # Chuyển đổi từ số sang tên chuỗi Enum
        result = [{"user_role": UserRole(role[0]).name} for role in user_roles]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route('/update-book/<int:book_id>', methods=['POST'])
@admin_required
def update_book(book_id):
    try:
        updated_data = request.get_json()

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'message': 'Book not found'}), 404

        book.title = updated_data.get('title', book.title)
        book.author = updated_data.get('author', book.author)

        genre_id = updated_data.get('genre_id')  # Lấy genre_id từ request
        if genre_id:
            genre = BookGerne.query.get(genre_id)  # Tìm thể loại theo ID
            if genre:
                book.book_gerne_id = genre.book_gerne_id  # Cập nhật ID của thể loại
            else:
                return jsonify({'success': False, 'message': f"Genre with ID '{genre_id}' not found"}), 400

        barcode = updated_data.get('barcode')
        if barcode:
            existing_book = Book.query.filter_by(barcode=barcode).first()
            if existing_book and existing_book.book_id != book.book_id:
                return jsonify({'success': False, 'message': f"Barcode '{barcode}' already exists"}), 400
            book.barcode = barcode

        publisher_name = updated_data.get('publisher')
        if publisher_name:
            publisher = Publisher.query.filter_by(publisher_name=publisher_name).first()
            if publisher:
                book.publisher_id = publisher.publisher_id
            else:
                return jsonify({'success': False, 'message': f"Publisher '{publisher_name}' not found"}), 400

        book.price = updated_data.get('price', book.price)
        book.num_page = updated_data.get('num_page', book.num_page)
        book.weight = updated_data.get('weight', book.weight)
        book.format = updated_data.get('format', book.format)
        book.dimension = updated_data.get('dimension', book.dimension)

        db.session.commit()

        return jsonify({'success': True, 'updated': updated_data})

    except Exception as e:
        app.logger.error(f"Error updating book: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"success": False, "message": "Book not found"}), 404

        db.session.delete(book)
        db.session.commit()

        return jsonify({"success": True})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


