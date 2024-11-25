from app.dao.OrderDAO import *
from flask import Blueprint
from flask import render_template, request
import json

order_api_bp = Blueprint('/api/v1/order', __name__)


@order_api_bp.route("/", methods=['GET'])
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
    return orders


@order_api_bp.route("/<order_id>/update", methods=['POST'])
def update(order_id):
    update_order(order_id, request.json)
    return request.json


@order_api_bp.route("/add", methods=['POST'], endpoint='test_add')
def test_add():
    order_id = create_offline_order(request.json)
    return {
        'order_id': order_id
    }


@order_api_bp.route("/<order_id>/detail", methods=['GET', 'POST'])
def find(order_id):
    order = find_by_id(order_id)
    return order.to_dict()