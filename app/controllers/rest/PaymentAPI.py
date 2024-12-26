from datetime import datetime

from flask_login import current_user
from flask import request, redirect, Blueprint, jsonify

from app import app, db, VNPayConfig
from app.VNPayConfig import generate_vnpay_url
from app.authentication.login_required import customer_required_api
from app.dao.OrderDAO import find_by_id, find_order_by_id, update_order_status, find_order_by_user_and_id
from app.model.Order import OrderStatus, PaymentDetail
from app.dao.PaymentDAO import create_payment as create_payment_detail

payment_rest_bp = Blueprint('payment_rest', __name__)


@payment_rest_bp.route('/', methods=['POST'])
@customer_required_api
def generate_payment():
    order_id = request.args.get("orderId", type=int)
    order = find_order_by_user_and_id(current_user.get_id(), order_id)
    vnpay_url = generate_vnpay_url(order)
    
    return jsonify({
        "message": "SUCCESS",
        'status': 200,
        "vnpay_url": vnpay_url
    })


@payment_rest_bp.route('/payment-ipn', methods=['GET'])
def process_ipn():
    res = request.args.to_dict()
    return VNPayConfig.process_ipn(res)
