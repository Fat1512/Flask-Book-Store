from app.dao import UserDao
from app import login
from app.dao.OrderDAO import find_all, find_add_by_user_id
from app.dao.UserDao import find_user_address
from app.model.User import UserRole
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from flask import Blueprint
from app import db
from app.model.User import User
from app.model.Account import Account

account_bp = Blueprint('account', __name__)


@account_bp.route('/purchase', methods=['GET'])
def purchase():
    payment_status = request.args.get('vnp_ResponseCode', default=None)

    if payment_status:
        return redirect(f'http://127.0.0.1:5000/account/purchase?payment={payment_status}')

    status = request.args.get('type', type=int)

    order = find_add_by_user_id(current_user.get_id(), status, 1, 5)

    order_to_dict = [order.to_detail_dict() for order in order]
    is_success = request.args.get('payment', default=None)

    return render_template("profile/purchase.html", is_success=is_success, order=order_to_dict)


@account_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserDao.auth_user(username=username, password=password)
        if user:
            if user.user_role == UserRole.ADMIN:
                login_user(user=user)
                return redirect(url_for('admin.admin_home'))
            else:
                err_msg = "Vai trò không hợp lệ!"
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template('admin-login.html', err_msg=err_msg)


@account_bp.route("/admin-logout")
def admin_logout():
    logout_user()
    return redirect(url_for('account.admin_login'))


@account_bp.route('/employee-login', methods=['GET', 'POST'])
def employee_login():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserDao.auth_user(username=username, password=password)
        if user:
            login_user(user=user, remember=True)
            print("current user day ne", current_user.user_role)
            if user.user_role == UserRole.EMPLOYEE_SALE:
                return redirect(url_for('employee.checkout'))
            elif user.user_role == UserRole.EMPLOYEE_MANAGER_WAREHOUSE:
                return redirect(url_for('employee.checkout'))
            elif user.user_role == UserRole.EMPLOYEE_MANAGER:
                return redirect(url_for('employee.checkout'))
            else:
                err_msg = "Vai trò không hợp lệ!"
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template('employee-login.html', err_msg=err_msg)


# @account_bp.route("/employee-register", methods=['GET', 'POST'])
# def employee_register():
#     err_msg = ''
#     if request.method == 'POST':
#         password = request.form.get('password')
#         confirm = request.form.get('confirm')
#         username = request.form.get('username')
#         email = request.form.get('email')
#
#         if password == confirm:
#             if UserDao.check_exists(username=username, email=email):
#                 err_msg = 'Tên người dùng hoặc email đã tồn tại!'
#             else:
#                 data = request.form.copy()
#                 del data['confirm']
#
#                 # Lấy user_role từ input hidden (Tên của vai trò)
#                 user_role = request.form.get('user_role')
#
#                 avt_url = request.files.get('avt_url')
#
#                 optional_fields = ['sex', 'phone_number', 'date_of_birth', 'isActive', 'last_access']
#                 for field in optional_fields:
#                     data[field] = data.get(field, None)
#
#                 # Xóa user_role khỏi data để không bị truyền trùng
#                 if 'user_role' in data:
#                     del data['user_role']
#
#                 UserDao.add_employee(avt_url=avt_url, user_role=user_role, **data)
#
#                 return redirect(url_for('account.employee_login'))
#         else:
#             err_msg = 'Mật khẩu không khớp!'
#
#     return render_template('employee-register.html', err_msg=err_msg)


@account_bp.route("/employee-logout")
def employee_logout():
    logout_user()
    return redirect(url_for('account.employee_login'))


@account_bp.route("/login", methods=['GET', 'POST'])
def login_process():
    err_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        roles = [UserRole.CUSTOMER, UserRole.ADMIN, UserRole.EMPLOYEE_SALE, UserRole.EMPLOYEE_MANAGER,
                 UserRole.EMPLOYEE_MANAGER_WAREHOUSE]

        u = None
        for role in roles:
            u = UserDao.auth_user(username=username, password=password, role=role)
            if u:
                break

        if u:
            login_user(u)
            return redirect(url_for('index.index'))
        else:
            err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"

    return render_template("login.html", err_msg=err_msg)


@account_bp.route('/address')
def address():
    address_list = find_user_address(current_user.get_id())
    return render_template('profile/address.html', address_list=address_list)


@account_bp.route('/profile')
def profile():
    return render_template('profile/profileUser.html')


@account_bp.route("/register", methods=['get', 'post'])
def register_process():
    err_msg = ''
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        username = request.form.get('username')
        email = request.form.get('email')

        if password == confirm:
            if UserDao.check_exists(username=username, email=email):
                err_msg = 'Tên người dùng hoặc email đã tồn tại!'
            else:
                data = request.form.copy()
                del data['confirm']

                avt_url = request.files.get('avt_url')
                optional_fields = ['sex', 'phone_number', 'date_of_birth', 'isActive', 'last_access']
                for field in optional_fields:
                    data[field] = data.get(field, None)

                UserDao.add_user(avt_url=avt_url, **data)

                return redirect(url_for('account.login_process'))
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


@account_bp.route("/logout")
def logout_process():
    logout_user()
    return redirect('/')


@account_bp.route("/forgot", methods=['GET', 'POST'])
def forgot_process():
    err_msg = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if not email or not password or not confirm:
            err_msg = 'Vui lòng điền đầy đủ thông tin!'
        else:
            email = email.strip()
            # Truy vấn account dựa trên email
            account = db.session.query(Account).join(User).filter(User.email == email).first()
            if account is None:
                err_msg = 'Email không tồn tại!'
            elif password != confirm:
                err_msg = 'Mật khẩu và xác nhận mật khẩu không trùng khớp!'
            else:
                UserDao.update_password(username=account.username, password=password)
                return redirect(url_for('account.login_process'))

    return render_template("forgotpass.html", err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return UserDao.get_user_by_id(user_id)

# @app.route("/add-products")
# def add_products_process():
#     return render_template("employee-add-products.html")
#
#
# def admin_required(f):
#     def wrap(*args, **kwargs):
#         if not current_user.is_authenticated:
#             return redirect(url_for('admin_login'))
#         if current_user.user_role != UserRole.ADMIN:
#             return redirect(url_for('admin_login'))
#         return f(*args, **kwargs)
#     wrap.__name__ = f.__name__
#     return wrap
#
#
# @app.route("/admin-home")
# # @login_required
# @admin_required
# def admin_home():
#     return render_template("admin-home.html")
#
#
# @app.route("/admin-statistic")
# def admin_statistic():
#     return render_template("admin-statistic.html")


# @app.route('/admin-login', methods=['GET', 'POST'])
# def admin_login():
#     err_msg = ''
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         user = UserDao.auth_user(username=username, password=password, role=UserRole.ADMIN)
#         if user:
#             login_user(user=user)
#             return redirect('/admin-home')
#         else:
#             err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"
#
#     return render_template('admin-login.html', err_msg=err_msg)
#
#
# @app.route("/admin-logout")
# def admin_logout():
#     logout_user()
#     return redirect('/admin-login')
#
#
# @app.route("/login", methods=['get', 'post'])
# def login_process():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         u = UserDao.auth_user(username=username, password=password, role=UserRole.USER)
#
#         if not u:
#             u = UserDao.auth_user(username=username, password=password, role=UserRole.ADMIN)
#
#         if u:
#             login_user(u)
#             return redirect('/')
#         else:
#             err_msg = "Tên đăng nhập hoặc mật khẩu không đúng!"
#
#     return render_template("login.html", err_msg=err_msg)
#
#
# @app.route("/register", methods=['get', 'post'])
# def register_process():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         password = request.form.get('password')
#         confirm = request.form.get('confirm')
#
#         if password.__eq__(confirm):
#             data = request.form.copy()
#             del data['confirm']
#
#             avt_url = request.files.get('avt_url')
#             optional_fields = ['sex', 'phone_number', 'date_of_birth', 'isActive', 'last_access']
#             for field in optional_fields:
#                 data[field] = data.get(field, None)
#             UserDao.add_user(avt_url=avt_url, **data)
#
#             return redirect('/login')
#         else:
#             err_msg = 'Mật khẩu không đúng!'
#
#     return render_template('register.html', err_msg=err_msg)
#
#
# @app.route("/logout")
# def logout_process():
#     logout_user()
#     return redirect('/')
#
#
# @login.user_loader
# def load_user(user_id):
#     return UserDao.get_user_by_id(user_id)
