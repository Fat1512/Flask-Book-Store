from app.dao.OrderDAO import *
from app.dao.SearchDAO import search_book
from app.dao.FormImportDAO import find_form_imports
from app.dao.ConfigDAO import get_config
from flask import Blueprint
from datetime import datetime
from flask import render_template, request
import json

employee_bp = Blueprint('employee', __name__)


@employee_bp.route("/checkout")
def checkout():
    books = search_book(limit=12, page=1, gerne_id=1, order="desc")
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto

    return render_template("employee/employeeCheckout.html", books=books)


@employee_bp.route("/order")
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
                           sort_by=sort_by, sort_dir=sort_dir, order_type=order_type, start_date=start_date, end_date=end_date)


@employee_bp.route("/order/<order_id>/update")
def update_order(order_id):
    order = find_by_id(order_id)

    books = search_book(limit=12, page=1, gerne_id=1, order="desc")
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto
    return render_template("employee/employeeOrderUpdate.html", order=order, books=books)


@employee_bp.route("/order/<order_id>/detail")
def get_order_detail(order_id):
    order = find_by_id(order_id)
    today = datetime.utcnow()
    return render_template("employee/employeeOrderDetail.html", order=order, today=today)


@employee_bp.route("/category")
def get_category():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        categories = data[0:4]
    return categories


@employee_bp.route("/import")
def import_book():
    books = search_book(limit=app.config['PAGE_SIZE'] + 10, page=1)
    book_dto = []

    for book in books['books']:
        book_dto.append(book.to_dict_manage())

    books['books'] = book_dto
    config = get_config()
    return render_template("employee/employeeImport.html", books=books, config=config)


@employee_bp.route("/import/history")
def import_book_history():
    page = request.args.get("page", 1, type=int)
    start_date = request.args.get("startDate", type=str)
    end_date = request.args.get("endDate", type=str)

    form_imports = find_form_imports(page=page, start_date=start_date, end_date=end_date)
    form_imports['form_imports'] = [form_import.to_dict() for form_import in form_imports['form_imports']]

    return render_template("employee/employeeImportHistory.html", form_imports=form_imports, end_date=end_date,
                           start_date=start_date, page=page)
