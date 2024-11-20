from flask import Blueprint
from flask import render_template, request
import json

employee_bp = Blueprint('employee', __name__)


@employee_bp.route("/")
def index():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        category_section = data[4:8]
    advertised_category_image = [
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746970/tvy6sddbfpmg7y28ny3j.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/yin3pb2nwlk7bqeqcjpx.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/mtfd7avuzgrpuotg7aej.webp',
        'https://res.cloudinary.com/dq27ted4k/image/upload/v1731746969/rw19jx9s8295npm171bm.webp'
    ]
    idx = 0
    for category in category_section:
        category['advertised_image'] = advertised_category_image[idx]
        idx += 1

    with open('data/new_release.json', encoding="utf8") as f:
        data = json.load(f)
        new_release = data[0:8]

    with open('data/bestselling_book.json', encoding="utf8") as f:
        data = json.load(f)
        bestselling_books = data[0:5]

    return render_template("home.html",
                           bestselling_books=bestselling_books,
                           new_release=new_release,
                           category_section=category_section)

@employee_bp.route("/checkout")
def checkout():
    return render_template("employee_checkout.html")


@employee_bp.route("/order")
def get_order():
    return render_template("employee.html")


@employee_bp.route("/order/update")
def update_order():
    request.args.get("order_id")
    order = None
    return render_template("employee-order-update.html", order=order)

@employee_bp.route("/order/detail")
def get_order_detail():
    request.args.get("order_id")
    order = None
    return render_template("employee-order-detail.html", order=order)

@employee_bp.route("/category")
def get_category():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        categories = data[0:4]

    return categories
