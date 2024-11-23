from app.dao.OrderDAO import *
from flask import Blueprint
from flask import render_template, request
import json

employee_bp = Blueprint('employee', __name__)


@employee_bp.route("/checkout")
def checkout():
    return render_template("employee_checkout.html")


@employee_bp.route("/order")
def get_order():
    status = request.args.get("status")
    paymentMethod = request.args.get("paymentMethod")
    sortBy = request.args.get("sortBy")
    sortDir = request.args.get("dir")
    page = request.args.get("page", 1)
    orders = find_all(status=status,
                      paymentMethod=paymentMethod,
                      sortBy=sortBy,
                      sortDir=sortDir,
                      page=int(page))
    orders['orders'] = [order.to_dict() for order in orders['orders']]
    return render_template("employee-order.html", orders=orders, status=status, paymentMethod=paymentMethod,
                           sortBy=sortBy, sortDir=sortDir)


@employee_bp.route("/order/update")
def update_order():
    request.args.get("order_id")
    order = None
    return render_template("employee-order-update.html", order=order)


@employee_bp.route("/order/<order_id>/detail")
def get_order_detail(order_id):
    order = find_by_id(order_id)
    return render_template("employee-order-detail.html", order=order.to_dict())


@employee_bp.route("/category")
def get_category():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        categories = data[0:4]

    return categories
