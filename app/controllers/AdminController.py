import pdb

import app.dao.BookGerneDAO
import app.utils.admin
from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import total_revenue_per_gerne, book_statistic_frequency, account_management, book_management, stats_revenue_by_month, stats_revenue_offline_by_month
from app.utils.admin import bookgerne_management, profile, stats_revenue_online_by_month, count_book, count_book_gerne, count_account, stats_sales_count_by_month, top_5_best_selling_books
from datetime import datetime
import math
from app import app, db
from app.model.BookGerne import BookGerne
from app.model.User import User
from app.model.Book import Book
from app.model.Account import Account
import hashlib
from app.model.Publisher import Publisher
from app.dao.BookGerneDAO import add_gerne,remove_gerne
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
    total_revenue = total_revenue_per_gerne()
    book = count_book()
    book_gerne = count_book_gerne()
    account = count_account()
    top_books = top_5_best_selling_books()
    return render_template("admin-home.html",total_revenue=total_revenue, book=book, book_gerne=book_gerne, account=account, top_books=top_books)


@admin_bp.route("/add-products")
def add_products_process():
    return render_template("employee-add-products.html")


@admin_bp.route("/book-manager")
@admin_required
def admin_book_manager():
    gerne_id = request.args.get('gerne_id', type=int)
    kw = request.args.get('kw')
    price_start = request.args.get('price_start', type=float)
    price_end = request.args.get('price_end', type=float)

    if gerne_id == 1:
        stats = book_management(kw=kw, price_start=price_start, price_end=price_end)
    else:
        stats = book_management(gerne_id, kw=kw, price_start=price_start, price_end=price_end)

    page = int(request.args.get('page', 1))
    page_size = app.config['BOOK_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    # Render template
    return render_template(
        "admin-book-manager.html",
        stats=paginated_stats, full_stats=stats, kw=kw,price_start=price_start, price_end=price_end,
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
    year = request.args.get('year', datetime.now().year, type=int)

    stats = book_gerne_statistic(kw=kw, selected_month=selected_month)
    stats_month = stats_revenue_by_month(year=year)

    page = int(request.args.get('page', 1))
    page_size = app.config['STATISTIC_REVEN_PAGE_SIZE']
    total = len(stats)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]


    total_revenue = total_revenue_per_gerne(kw=kw, selected_month=selected_month)

    return render_template(
        "admin-statistic-revenue.html",
        stats=paginated_stats,
        full_stats=stats,
        stats_month=stats_month,
        full_stats_month=stats_month,
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
    selected_month = request.args.get('selected_month')

    genres = db.session.query(BookGerne).all()

    # Tạo từ điển genres_dict với ID là khóa và tên là giá trị
    genres_dict = {genre.book_gerne_id: genre.name for genre in genres}

    if gerne_id == 1:
        stats = book_statistic_frequency(selected_month=selected_month)
        statss = book_statistic_frequency(selected_month=selected_month)
    else:
        stats = book_statistic_frequency(gerne_id, selected_month=selected_month)
        statss = book_statistic_frequency(gerne_id, selected_month=selected_month)

    page = int(request.args.get('page', 1))
    page_size = app.config['STATISTIC_FRE_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    # Render template
    return render_template(
        "admin-statistic-frequency.html",
        stats=paginated_stats, full_stats=stats, statss=statss, genres=genres, genres_dict=genres_dict,
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
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    stats = account_management(user_role, first_name=first_name, last_name=last_name)

    page = int(request.args.get('page', 1))
    page_size = app.config['STATISTIC_FRE_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]

    return render_template(
        "admin-account-manager.html",
        stats=paginated_stats,first_name=first_name, last_name=last_name,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )


@admin_bp.route("/bookgerne-manager")
@admin_required
def admin_bookgerne_manager():
    kw = request.args.get('kw')
    stats = bookgerne_management(kw=kw)

    genres = db.session.query(BookGerne).all()
    genres_dict = {genre.book_gerne_id: genre.name for genre in genres}

    page = int(request.args.get('page', 1))
    page_size = app.config['BOOK_PAGE_SIZE']
    total = len(stats)

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_stats = stats[start_idx:end_idx]
    return render_template("admin-bookgerne-manager.html",
        kw=kw,
        stats=paginated_stats, genres_dict=genres_dict,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        })


@admin_bp.route("/profile")
@admin_required
def admin_profile():
    profile_data = profile()
    current_year = datetime.now().year
    return render_template("admin-profile.html", profile=profile_data, current_year=current_year)


@admin_bp.route("/statistic")
@admin_required
def admin_statistic():
    return render_template("admin-statistic.html")


@admin_bp.route('/api/revenue-online', methods=['GET'])
def get_revenue_online():
    data = stats_revenue_online_by_month()
    print("Data from stats_revenue_online_by_month:", data)
    return jsonify(data)

@admin_bp.route('/api/revenue-offline', methods=['GET'])
def get_revenue_offline():
    data = stats_revenue_offline_by_month()
    print("Data from stats_revenue_offline_by_month:", data)
    return jsonify(data)

@admin_bp.route('/api/sales_count', methods=['GET'])
def get_sales_count():
    data = stats_sales_count_by_month()  # Lấy dữ liệu cho năm hiện tại
    print("Data from stats_sales_count_by_month:", data)
    return jsonify(data)

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


@admin_bp.route("/api/user_roles_employee", methods=["GET"])
def get_user_roles_employee():
    try:
        employee_roles = [
            UserRole.EMPLOYEE_SALE,
            UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
            UserRole.EMPLOYEE_MANAGER,
        ]
        result = [{"user_role": role.name, "role_id": role.value} for role in employee_roles]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@admin_bp.route('/update-book/<int:book_id>', methods=['POST'])
@admin_required
def update_book(book_id):
    try:
        updated_data = request.get_json()
        print("Received data:", updated_data)
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'message': 'Book not found'}), 404

        book.title = updated_data.get('title', book.title)
        book.author = updated_data.get('author', book.author)
        book.book_gerne_id = updated_data.get('gerne', book.book_gerne_id)

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


@admin_bp.route('/add-bookgerne', methods=['POST'])
@admin_required
def add_bookgerne():
    # try:
        data = request.json

        name = data.get('name')
        gerne_id = int(data.get('parent_id'))

        add_gerne(name,gerne_id)



        return jsonify({'success': True, 'message': 'Thể loại mới đã được thêm'})


@admin_bp.route('/update-bookgerne/<int:book_gerne_id>', methods=['POST'])
@admin_required
def update_bookgerne(book_gerne_id):
    try:
        updated_data = request.get_json()

        bookgerne = BookGerne.query.get(book_gerne_id)
        if not bookgerne:
            return jsonify({'success': False, 'message': 'Book genre not found'}), 404

        bookgerne.name = updated_data.get('name', bookgerne.name)
        bookgerne.lft = updated_data.get('lft', bookgerne.lft)
        bookgerne.rgt = updated_data.get('rgt', bookgerne.rgt)

        db.session.commit()

        return jsonify({'success': True, 'updated': {
            'book_gerne_id': book_gerne_id,
            'name': bookgerne.name,
            'lft': bookgerne.lft,
            'rgt': bookgerne.rgt
        }})

    except Exception as e:
        app.logger.error(f"Error updating book genre with ID {book_gerne_id}: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal Server Error'}), 500


@admin_bp.route('/delete-bookgerne/<int:book_gerne_id>', methods=['POST'])
@admin_required
def delete_bookgerne(book_gerne_id):
    remove_gerne(int(book_gerne_id))
    return jsonify({"success": True})
    # try:
    #     bookgerne = BookGerne.query.get(book_gerne_id)
    #     if not bookgerne:
    #         return jsonify({"success": False, "message": "Book genre not found"}), 404
    #
    #     db.session.delete(bookgerne)
    #     db.session.commit()
    #
    #     return jsonify({"success": True})
    #
    # except Exception as e:
    #     db.session.rollback()
    #     app.logger.error(f"Error deleting book genre: {str(e)}")
    #     return jsonify({"success": False, "message": "Internal server error", "error": str(e)}), 500


@admin_bp.route('/update-profile', methods=['POST'])
@admin_required
def update_profile():
    data = request.get_json()

    try:
        # Lấy thông tin người dùng từ current_user
        user = User.query.filter_by(user_id=current_user.user_id).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Cập nhật thông tin người dùng từ dữ liệu client gửi lên
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.sex = data.get('sex', user.sex)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.avt_url = data.get('avt_url', user.avt_url)

        # Lưu các thay đổi vào cơ sở dữ liệu
        db.session.commit()

        return jsonify({"success": True, "updated": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/add-employee', methods=['POST'])  # Cập nhật đường dẫn ở đây
@admin_required
def add_employee():
    try:
        data = request.json
        print(f"Received data: {data}")

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_role = data.get('user_role')

        # if not username or not email or not password or not user_role:
        #     return jsonify({'success': False, 'message': 'Thiếu dữ liệu'}), 400

        if User.query.join(Account).filter(Account.username.__eq__(username)).first() or User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Tên người dùng hoặc email đã tồn tại!'}), 400

        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        new_user = User(first_name=first_name,last_name=last_name,email=email, user_role=user_role)
        new_account = Account(username=username,password=hashed_password)
        new_user.account.append(new_account)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Đăng ký nhân viên thành công'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Lỗi khi đăng ký nhân viên: {str(e)}")
        return jsonify({'success': False, 'message': 'Lỗi server', 'error': str(e)}), 500
