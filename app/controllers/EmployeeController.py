from app.dao.OrderDAO import *
from app.dao.SearchDAO import searchBook
from app.dao.ConfigDAO import get_config
from flask import Blueprint
from datetime import datetime
from flask import render_template, request
import json

employee_bp = Blueprint('employee', __name__)


@employee_bp.route("/checkout")
def checkout():
    books = searchBook(limit=8, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto

    return render_template("employee-checkout.html", books=books)


@employee_bp.route("book/import")
def import_book():
    books = searchBook(limit=15, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict_manage())
    books['books'] = book_dto
    config = get_config()
    return render_template("employee-import.html", books=books, config=config)


@employee_bp.route("/order")
def get_order():
    status = request.args.get("status")
    payment_method = request.args.get("paymentMethod")
    sort_by = request.args.get("sortBy")
    sort_dir = request.args.get("dir")
    order_type = request.args.get("orderType")
    page = request.args.get("page", 1)

    orders = find_all(status=status,
                      payment_method=payment_method,
                      sort_by=sort_by,
                      sort_dir=sort_dir,
                      order_type=order_type,
                      page=int(page))
    return render_template("employee-order.html", orders=orders, status=status, paymentMethod=payment_method,
                           sortBy=sort_by, sortDir=sort_dir, orderType=order_type)


@employee_bp.route("/order/<order_id>/update")
def update_order(order_id):
    order = find_by_id(order_id)

    books = searchBook(limit=8, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto
    return render_template("employee-order-update.html", order=order, books=books)


@employee_bp.route("/order/<order_id>/detail")
def get_order_detail(order_id):
    order = find_by_id(order_id)
    today = datetime.utcnow()
    return render_template("employee-order-detail.html", order=order, today=today)

@employee_bp.route("/category")
def get_category():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        categories = data[0:4]
    return categories