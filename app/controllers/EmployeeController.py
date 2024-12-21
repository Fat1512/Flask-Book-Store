from app.dao.OrderDAO import *
from app.dao.SearchDAO import search_book
from app.dao.FormImportDAO import find_form_imports
from app.dao.ConfigDAO import get_config
from flask import Blueprint
from datetime import datetime
from flask import render_template, request
import json
from app.model.User import UserRole
from app.model.Publisher import Publisher
from app.model.User import User
from flask import jsonify
from flask import render_template, redirect, url_for, request
from flask_login import current_user
from app.utils.admin import book_management

employee_bp = Blueprint('employee', __name__)


def employee_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap



def employee_sale_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_SALE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def employee_manager_warehouse_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER_WAREHOUSE, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def employee_manager_required(f):
    def wrap(*args, **kwargs):
        print("yest1", current_user.is_authenticated)
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_MANAGER, UserRole.ADMIN]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@employee_bp.route("/checkout")
@employee_sale_required
def checkout():
    books = search_book(limit=12, page=1, gerne_id=1, order="desc")
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto

    return render_template("employee/employeeCheckout.html", books=books)


@employee_bp.route("/order")
@employee_sale_required
def get_order():
    status = request.args.get("status")
    payment_method = request.args.get("paymentMethod")
    sort_by = request.args.get("sortBy")
    sort_dir = request.args.get("dir")
    order_type = request.args.get("orderType")
    page = request.args.get("page", 1)

    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    orders = find_all(status=status,
                      payment_method=payment_method,
                      sort_by=sort_by,
                      sort_dir=sort_dir,
                      order_type=order_type,
                      page=int(page),
                      start_date=start_date,
                      end_date=end_date)
    return render_template("employee/employeeOrder.html", orders=orders, status=status, payment_method=payment_method,
                           sort_by=sort_by, sort_dir=sort_dir, order_type=order_type, start_date=start_date,
                           end_date=end_date)


@employee_bp.route("/order/<order_id>/update")
@employee_sale_required
def update_order(order_id):
    order = find_by_id(order_id)

    books = search_book(limit=12, page=1, gerne_id=1, order="desc")
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto
    return render_template("employee/employeeOrderUpdate.html", order=order, books=books)


@employee_bp.route("/order/<order_id>/detail")
@employee_sale_required
def get_order_detail(order_id):
    order = find_by_id(order_id)
    today = datetime.utcnow()
    return render_template("employee/employeeOrderDetail.html", order=order, today=today)


@employee_bp.route("/import")
@employee_manager_warehouse_required
def import_book():
    books = search_book(limit=app.config['PAGE_SIZE'] + 10, page=1)
    book_dto = []

    for book in books['books']:
        book_dto.append(book.to_dict_manage())

    books['books'] = book_dto
    config = get_config()
    return render_template("employee/employeeImport.html", books=books, config=config)


@employee_bp.route("/import/history")
@employee_manager_warehouse_required
def import_book_history():
    page = request.args.get("page", 1, type=int)
    start_date = request.args.get("startDate", type=str)
    end_date = request.args.get("endDate", type=str)

    form_imports = find_form_imports(page=page, start_date=start_date, end_date=end_date)
    form_imports['form_imports'] = [form_import.to_dict() for form_import in form_imports['form_imports']]

    return render_template("employee/employeeImportHistory.html", form_imports=form_imports, end_date=end_date,
                           start_date=start_date, page=page)


@employee_bp.route("/add-products")
@employee_manager_required
def add_products_process():
    return render_template("employee/employeeAddProducts.html")


@employee_bp.route("/book-manager")
@employee_manager_required
def book_manager():
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
        "/employee/employeeBookManager.html",
        stats=paginated_stats, full_stats=stats, kw=kw, price_start=price_start, price_end=price_end,
        books={
            'current_page': page,
            'total_page': math.ceil(total / page_size),
            'pages': range(1, math.ceil(total / page_size) + 1),
        }
    )


@employee_bp.route('/update-book/<int:book_id>', methods=['POST'])
@employee_manager_required
def update_book(book_id):
    updated_data = request.get_json()
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


@employee_bp.route('/delete-book/<int:book_id>', methods=['POST'])
@employee_manager_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"success": True})


@employee_bp.route("/profile")
@employee_required
def employee_profile():
    return render_template("/employee/employeeProfile.html")


@employee_bp.route('/update-profile', methods=['POST'])
@employee_required
def update_profile():
    data = request.get_json()

    try:
        user = User.query.filter_by(user_id=current_user.user_id).first()

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.sex = data.get('sex', user.sex)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.avt_url = data.get('avt_url', user.avt_url)

        db.session.commit()

        return jsonify({"success": True, "updated": data}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
