import pdb

from flask_login import current_user

from app.dao.CartDao import delete_cart_item
from app.dao.OrderDAO import *
from app.dao.PaymentDAO import create_payment
from app.dao.UserDao import *
from app.dao.FormImportDAO import *
from flask import Blueprint, jsonify
from flask import render_template, request
from app.controllers.EmployeeController import employee_required

order_api_bp = Blueprint('/api/v1/order', __name__)


@order_api_bp.route("/", methods=['GET'])
def get_order():
    status = None
    if request.args.get("status"):
        status = request.args.get("status").split(',')
    payment_method = request.args.get("paymentMethod")
    order_id = request.args.get("orderId")
    sort_by = request.args.get("sortBy")
    sort_dir = request.args.get("dir")
    order_type = request.args.get("orderType")
    page = request.args.get("page", 1)
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    orders = find_all(order_id=order_id,
                      status=status,
                      payment_method=payment_method,
                      sort_by=sort_by,
                      sort_dir=sort_dir,
                      order_type=order_type,
                      page=int(page),
                      start_date=start_date,
                      end_date=end_date)
    return jsonify({
        "message": "Success",
        "status": 200,
        "data": orders
    })


@order_api_bp.route("/<int:order_id>/update", methods=['POST'])
@employee_required
def update(order_id):
    update_order(order_id, request.json)
    return jsonify({
        "message": "Success",
        "status": 200,
        "data": request.json
    })


@order_api_bp.route("/add", methods=['POST'], endpoint='test_add')
@employee_required
def offline_order():
    order_list = request.json['orderList']
    customer_info = request.json['customerInfo']

    user = None
    if bool(customer_info):
        user = find_by_customer_id_phone_number(int(customer_info['id']), str(customer_info['phone_number']))

    employee_id = current_user.get_id()
    order = create_offline_order(order_list=order_list, user=user, employee_id=employee_id)

    return jsonify({
        "message": "Successfully Created",
        "status": 200,
        "data": order
    })


@order_api_bp.route('/onlineOrder', methods=['POST'])
def online_order():
    data = request.json
    order = create_online_order(current_user.get_id(), data)

    for book in data['books']:
        delete_cart_item(current_user.get_id(), book['bookId'])

    return jsonify({
        "message": "Success",
        "status": 200,
        "orderId": order.order_id
    })


@order_api_bp.route('/orderCancellation', methods=['POST'])
def cancel_order():
    data = request.json
    order_cancellation = create_order_cancellation(data)

    return jsonify({
        'message': 'Hủy thành công',
        'status': 200,
        'data': order_cancellation.to_dict()
    })


@order_api_bp.route("/<order_id>/status", methods=['POST'])
@employee_required
def update_status(order_id):
    status = request.json.get("orderStatusId")
    status_enum = OrderStatus(int(status))

    order = update_order_status(order_id, status_enum)

    if OrderStatus.DA_HOAN_THANH == order.status and PaymentMethod.TIEN_MAT == order.payment_method:
        total_amount = calculate_total_order_amount(order_id)
        payment_detail = PaymentDetail(order_id=order.order_id, created_at=datetime.utcnow(), amount=total_amount)
        create_payment(payment_detail)

    return jsonify({
        'message': 'Cập nhật thành công',
        'status': 200
    })


@order_api_bp.route("/<order_id>/detail", methods=['GET', 'POST'])
def find(order_id):
    order = find_by_id(order_id)

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': order
    })
