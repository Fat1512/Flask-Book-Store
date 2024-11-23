from app.dao.OrderDAO import *
from flask import Blueprint
from flask import render_template, request
import json

order_api_bp = Blueprint('order_api', __name__)

@order_api_bp.route("/")
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
    # orders['orders'] = [order.to_dict() for order in orders['orders']]
    return orders