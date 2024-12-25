from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user
from flask import redirect, request
import pdb

import app.dao.BookGerneDAO
import app.model.Config
import app.utils.admin
from app.model.User import UserRole
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from app.utils.admin import book_gerne_statistic
from flask import jsonify
from app.utils.admin import total_revenue_per_gerne, book_statistic_frequency, account_management, book_management, \
    stats_revenue_by_month, stats_revenue_offline_by_month
from app.utils.admin import bookgerne_management, config, stats_revenue_online_by_month, count_book, count_book_gerne, \
    count_account, stats_sales_count_by_month, top_5_best_selling_books
from datetime import datetime
import math
from app import app, db
from app.model.BookGerne import BookGerne
from app.model.User import User
from app.model.Book import Book
from app.model.Account import Account
import hashlib
from app.model.Publisher import Publisher
from app.dao.BookGerneDAO import add_gerne, remove_gerne
from app.model.Config import Config


# class AuthenticatedAdmin(ModelView):
#     def is_accessible(self):
#         if current_user.is_authenticated:
#             return current_user.user_role == UserRole.ADMIN
#         return False
# 
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('account.admin_login', next=request.url))


def admin_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.admin_login'))
        if current_user.user_role != UserRole.ADMIN:
            return redirect(url_for('account.admin_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


class AdminHome(AdminIndexView):
    @expose("/")
    @admin_required
    def index(self):
        total_revenues = total_revenue_per_gerne()
        total_books = count_book()
        total_genres = count_book_gerne()
        total_accounts = count_account()
        online_revenue = stats_revenue_online_by_month()
        offline_revenue = stats_revenue_offline_by_month()
        sales_count = stats_sales_count_by_month()
        top_books = top_5_best_selling_books()

        return self.render(
            "/admin/adminHome.html",
            total_revenues=total_revenues,
            total_books=total_books,
            total_genres=total_genres,
            total_accounts=total_accounts,
            online_revenue=online_revenue,
            offline_revenue=offline_revenue,
            sales_count=sales_count,
            top_books=top_books,
        )


class AdminStatisticRevenue(ModelView):
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def admin_statistic_revenue(self):
        # Lấy tham số từ request
        kw = request.args.get('kw')
        selected_month = request.args.get('selected_month')
        year = request.args.get('year', datetime.now().year, type=int)

        # Lấy các thống kê
        stats = book_gerne_statistic(kw=kw, selected_month=selected_month)
        stats_month = stats_revenue_by_month(year=year)

        # Phân trang
        page = int(request.args.get('page', 1))
        page_size = app.config['STATISTIC_REVEN_PAGE_SIZE']
        total = len(stats)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_stats = stats[start_idx:end_idx]

        total_revenue = total_revenue_per_gerne(kw=kw, selected_month=selected_month)

        # Truyền dữ liệu vào template
        return self.render(
            "/admin/adminStatisticRevenue.html",
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


class AdminStatisticFrequency(ModelView):
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def admin_statistic_frequency(self):
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

        return self.render(
            "/admin/adminStatisticFrequency.html",
            stats=paginated_stats, full_stats=stats, statss=statss, genres=genres, genres_dict=genres_dict,
            books={
                'current_page': page,
                'total_page': math.ceil(total / page_size),
                'pages': range(1, math.ceil(total / page_size) + 1),
            }
        )


class AdminAccountManager(ModelView):
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def admin_account_manager(self):
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

        return self.render(
            "/admin/adminAccountManager.html",
            stats=paginated_stats, first_name=first_name, last_name=last_name,
            books={
                'current_page': page,
                'total_page': math.ceil(total / page_size),
                'pages': range(1, math.ceil(total / page_size) + 1),
            }
        )


# class AdminBookGerneManager(ModelView):
#     @expose("/", methods=("GET", "POST"))
#     @admin_required
#     def admin_bookgerne_manager(self):
#         kw = request.args.get('kw')
#         stats = bookgerne_management(kw=kw)
#
#         genres = db.session.query(BookGerne).all()
#         genres_dict = {genre.book_gerne_id: genre.name for genre in genres}
#
#         page = int(request.args.get('page', 1))
#         page_size = app.config['BOOK_PAGE_SIZE']
#         total = len(stats)
#
#         start_idx = (page - 1) * page_size
#         end_idx = start_idx + page_size
#         paginated_stats = stats[start_idx:end_idx]
#
#         return self.render(
#             "/admin/adminBookGerneManager.html",
#             kw=kw,
#             stats=paginated_stats, genres_dict=genres_dict,
#             books={
#                 'current_page': page,
#                 'total_page': math.ceil(total / page_size),
#                 'pages': range(1, math.ceil(total / page_size) + 1),
#             })


class AdminConfig(ModelView):
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def admin_config(self):
        c = config()
        return self.render("/admin/adminConfig.html", c=c)


class AdminProfile(ModelView):
    @expose("/", methods=("GET", "POST"))
    @admin_required
    def admin_profile(self):
        return self.render("/admin/adminProfile.html")


admin = Admin(app=app, name='ok', index_view=AdminHome())
admin.add_view(AdminStatisticRevenue(BookGerne, db.session, name='Statistic Revenue', endpoint='statistic-revenue',
                                     url="/admin/statistic-revenue"))
admin.add_view(
    AdminStatisticFrequency(BookGerne, db.session, name='Statistic Frequency', endpoint='statistic-frequency',
                            url="/admin/statistic-frequency"))
admin.add_view(AdminAccountManager(BookGerne, db.session, name='Account Manager', endpoint='account-manager',
                                   url="/admin/account-manager"))
# admin.add_view(
#     AdminBookGerneManager(BookGerne, db.session, name='Bookgerne Manager', endpoint='bookgerne-manager',
#                           url="/admin/bookgerne-manager"))
admin.add_view(
    AdminConfig(BookGerne, db.session, name='Config', endpoint='config',
                url="/admin/config"))

admin.add_view(
    AdminProfile(BookGerne, db.session, name='Profile', endpoint='profile',
                 url="/admin/profile"))


@app.route('/api/revenue-online', methods=['GET'])
def get_revenue_online():
    data = stats_revenue_online_by_month()
    print("Data from stats_revenue_online_by_month:", data)
    return jsonify(data)


@app.route('/api/revenue-offline', methods=['GET'])
def get_revenue_offline():
    data = stats_revenue_offline_by_month()
    print("Data from stats_revenue_offline_by_month:", data)
    return jsonify(data)


@app.route('/api/sales_count', methods=['GET'])
def get_sales_count():
    data = stats_sales_count_by_month()  # Lấy dữ liệu cho năm hiện tại
    print("Data from stats_sales_count_by_month:", data)
    return jsonify(data)


@app.route("/api/gernes", methods=["GET"])
def get_gernes():
    gernes = db.session.query(BookGerne.book_gerne_id, BookGerne.name).all()
    return jsonify([{"id": gerne.book_gerne_id, "name": gerne.name} for gerne in gernes])


@app.route("/api/user_roles", methods=["GET"])
def get_user_roles():
    try:
        user_roles = db.session.query(User.user_role).distinct().all()

        # Chuyển đổi từ số sang tên chuỗi Enum
        result = [{"user_role": UserRole(role[0]).name} for role in user_roles]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/user_roles_employee", methods=["GET"])
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


@app.route('/add-bookgerne', methods=['POST'])
def add_bookgerne():
    data = request.json

    name = data.get('name')
    gerne_id = int(data.get('parent_id'))

    add_gerne(name, gerne_id)

    return jsonify({'success': True, 'message': 'Thể loại mới đã được thêm'})


@app.route('/update-bookgerne/<int:book_gerne_id>', methods=['POST'])
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


@app.route('/delete-bookgerne/<int:book_gerne_id>', methods=['POST'])
def delete_bookgerne(book_gerne_id):
    remove_gerne(int(book_gerne_id))
    return jsonify({"success": True})


@app.route('/add-employee', methods=['POST'])  # Cập nhật đường dẫn ở đây
def add_employee():
    try:
        data = request.json

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_role = data.get('user_role')

        if User.query.join(Account).filter(Account.username.__eq__(username)).first() or User.query.filter_by(
                email=email).first():
            return jsonify({'success': False, 'message': 'Tên người dùng hoặc email đã tồn tại!'}), 400

        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        new_user = User(first_name=first_name, last_name=last_name, email=email, user_role=user_role)

        new_account = Account(username=username, password=hashed_password)

        new_user.account = new_account

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Đăng ký nhân viên thành công'})

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Lỗi khi đăng ký nhân viên: {str(e)}")
        return jsonify({'success': False, 'message': 'Lỗi server', 'error': str(e)}), 500


@app.route('/update-config', methods=['POST'])
def update_config():
    data = request.get_json()

    try:
        c = Config.query.first()

        if not c:
            return jsonify({"success": False, "message": "User not found"}), 404

        c.min_restock_qty = data.get('quantity', c.min_restock_qty)
        c.min_restock_level = data.get('level', c.min_restock_level)
        c.order_cancel_period = data.get('cancel', c.order_cancel_period)

        db.session.commit()

        return jsonify({"success": True, "updated": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
