from datetime import datetime

from flask import request, redirect, Blueprint, jsonify

from app import app, db
from app.VNPayConfig import generate_vnpay_url, validate_vnpay_response
from app.dao.OrderDAO import find_by_id, find_order_by_id, update_order_status
from app.model.Order import OrderStatus, PaymentDetail
from app.dao.PaymentDAO import create_payment as create_payment_detail

payment_rest_bp = Blueprint('payment_rest', __name__)


@payment_rest_bp.route('/', methods=['POST'])
def generate_payment():
    order_id = request.args.get("orderId", type=int)
    order = find_order_by_id(order_id)
    vnpay_url = generate_vnpay_url(order)
    return jsonify({
        "message": "SUCCESS",
        'status': 200,
        "vnpay_url": vnpay_url
    })


@payment_rest_bp.route('/return', methods=['GET'])
def payment_return():
    response_data = request.args.to_dict()

    # Validate the response
    if not validate_vnpay_response(response_data):
        pass

    order_id = response_data.get('orderId')
    response_code = response_data.get('vnp_ResponseCode')
    order = find_order_by_id(order_id)

    payment_detail = PaymentDetail(order_id=order.order_id, created_at=datetime.utcnow(),
                                   amount=order.get_amount())
    create_payment_detail(payment_detail)

    if order:
        if response_code == '00':  # Payment success
            update_order_status(order_id, OrderStatus.DA_THANH_TOAN)
        else:  # Payment failed
            update_order_status(order_id, OrderStatus.DANG_CHO_THANH_TOAN)

    return redirect("http://127.0.0.1:5000//cart?payment=success")
