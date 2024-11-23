from app.dao.OrderDAO import *
from flask import Blueprint
from flask import render_template, request
import json

order_api_bp = Blueprint('order_api', __name__)

@order_api_bp.route("/")
def get_order():
    status = request.args.get("status")
    paymentMethod = request.args.get("payment-method")
    sortBy = request.args.get("sortBy")
    sortDir = request.args.get("sortDir")
    page = request.args.get("page", 1)
    orders = find_all(status=status,
             paymentMethod=paymentMethod,
             sortBy=sortBy,
             sortDir=sortDir,
             page=int(page))
    orders['orders'] = [order.to_dict() for order in orders['orders']]
    return orders