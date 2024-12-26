import pdb

from app.authentication.login_required import employee_sale_required, employee_manager_warehouse_required, \
    employee_manager_required, employee_required, employee_manager_required_api
from app.dao.OrderDAO import *
from app.model.Book import BookFormat
from app.dao.SearchDAO import search_book
from app.dao.FormImportDAO import find_form_imports
from app.dao.ConfigDAO import get_config
from app.dao.PublisherDAO import find_all as find_all_publisher
from flask import Blueprint
from datetime import datetime
from app.model.Publisher import Publisher
from flask import jsonify
from flask import render_template, redirect, url_for, request
from app.utils.admin import book_management, bookgerne_management
from app.utils.helper import FORMAT_BOOK_TEXT
from app.model.BookGerne import BookGerne

employee_bp = Blueprint('employee', __name__)

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
    try:
        order = find_by_id(order_id)

        allowed_status = [OrderStatus.DANG_XU_LY.value, OrderStatus.CHO_GIAO_HANG.value,
                          OrderStatus.DANG_CHO_NHAN.value]
        if order['order_type']['id'] != 1 or order['payment']['payment_method']['id'] is not PaymentMethod.TIEN_MAT.value or \
                order['status']['id'] not in allowed_status:
            return redirect(url_for('employee.get_order'))

        books = search_book(limit=12, page=1, gerne_id=1, order="desc")
        book_dto = []
        for book in books['books']:
            book_dto.append(book.to_dict())
        books['books'] = book_dto
        return render_template("employee/employeeOrderUpdate.html", order=order, books=books)

    except Exception as e:
        return redirect(url_for('employee.get_order'))


@employee_bp.route("/order/<order_id>/detail")
@employee_sale_required
def get_order_detail(order_id):
    try:
        order = find_by_id(order_id)
        today = datetime.utcnow()
        return render_template("employee/employeeOrderDetail.html", order=order, today=today)

    except Exception as e:
        return redirect(url_for('employee.get_order'))


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
    publishers = find_all_publisher()
    return render_template("employee/employeeAddProducts.html", publishers=publishers, formats=FORMAT_BOOK_TEXT)


@employee_bp.route("/book-manager")
@employee_manager_required_api
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

        format_value = updated_data.get('format')
        if format_value:
            try:
                if isinstance(format_value, int):  # Nếu là số
                    book.format = BookFormat(format_value)  # Chuyển trực tiếp từ số sang Enum
                elif format_value.startswith('BookFormat.'):  # Nếu là chuỗi dạng 'BookFormat.BIA_MEM'
                    book.format = BookFormat[format_value.split('BookFormat.')[1]]
                else:  # Nếu là chuỗi tên Enum như 'BIA_MEM'
                    book.format = BookFormat[format_value]
            except KeyError:
                return jsonify({'success': False, 'message': f"Invalid format value: {format_value}"}), 400

        book.price = updated_data.get('price', book.price)
        book.num_page = updated_data.get('num_page', book.num_page)
        book.weight = updated_data.get('weight', book.weight)
        # book.format = updated_data.get('format', book.format)
        book.dimension = updated_data.get('dimension', book.dimension)

        db.session.commit()

        return jsonify({'success': True, 'updated': updated_data})

    except Exception as e:
        app.logger.error(f"Error updating book: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@employee_bp.route('/delete-book/<int:book_id>', methods=['POST'])
@employee_manager_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"success": False, "message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({"success": True})


@employee_bp.route("/bookgerne-manager")
@employee_manager_required
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
    return render_template("/admin/adminBookGerneManager.html",
                           kw=kw,
                           stats=paginated_stats, genres_dict=genres_dict,
                           books={
                               'current_page': page,
                               'total_page': math.ceil(total / page_size),
                               'pages': range(1, math.ceil(total / page_size) + 1),
                           })


@employee_bp.route("/profile")
@employee_required
def employee_profile():
    return render_template("/employee/employeeProfile.html")
