import pdb

from app.dao.ConfigDAO import get_config
from app.exception.ConfictError import ConflictError
from app.exception.InsufficientError import InsufficientError
from app.exception.GeneralInsufficientError import GeneralInsufficientError
from app.exception.NotFoundError import NotFoundError
from app.exception.UnauthorizedAccessError import UnauthorizedAccess
from app.model.Book import Book
from app.model.Config import Config
from app.model.Order import Order, PaymentDetail, ShippingMethod, OrderCancellation
from sqlalchemy import desc, asc, func
from datetime import datetime, timedelta
from app import app, db
from app.model.Order import OrderStatus, PaymentMethod, OnlineOrder, OfflineOrder, OrderDetail
from decimal import *
import math

from app.model.User import UserRole


# find by id, find by sdt khach hang
# filter by status, PTTT
# sort by thoi gian dat, tong tien

def find_by_id(order_id):
    order = Order.query.get(order_id)

    if not order: raise NotFoundError("Không tìm thấy đơn")

    order = order.online_order.to_detail_dict() if order.online_order else order.offline_order.to_detail_dict()
    order['total_amount'] = calculate_total_order_amount(order_id)
    return order


def update_order_status(order_id, status):
    order = Order.query.get(order_id)

    if not order: raise NotFoundError("Không tìm thấy đơn để cập nhật")

    order.status = status
    db.session.commit()
    return order


def find_add_by_user_id(user_id, status, page, limit):
    order = Order.query
    order = order.filter(Order.customer_id == user_id)
    if status and status != 8:
        order = order.filter(Order.status == OrderStatus(int(status)))
    order = order.order_by(desc(Order.created_at))
    start = (page - 1) * limit
    end = start + limit
    order = order.slice(start, end)
    return order.all()


def create_order_cancellation(user, data):
    order = Order.query.get(data['orderId'])

    order = Order.query.filter(Order.order_id == data['orderId']).first()
    if user.user_roles == UserRole.CUSTOMER and order.user_id != user.get_id():
        raise UnauthorizedAccess("You don't have permission for resource")

    if order is None: raise NotFoundError("Không tìm thấy đơn hàng của bạn", 404)

    allowed_status = [OrderStatus.DANG_XU_LY, OrderStatus.CHO_GIAO_HANG, OrderStatus.DANG_CHO_NHAN,
                      OrderStatus.DANG_CHO_THANH_TOAN]
    if order.online_order is None and order.payment_method is not PaymentMethod.TIEN_MAT and order.status not in allowed_status:
        raise ConflictError("Điều kiện hủy đơn không đáp ứng")

    for order_detail in order.order_detail:
        order_detail.book.increase_book(quantity=order_detail.quantity)

    order_cancellation = OrderCancellation(order_id=order.order_id, reason=data['reason'])
    order.status = OrderStatus.DA_HUY
    db.session.add(order_cancellation)
    db.session.commit()

    return order_cancellation


def find_order_by_id(id):
    order = Order.query.get(id)
    if not order: raise NotFoundError("Không tìm thấy đơn để cập nhật")
    return order


def find_order_by_user_and_id(user_id, id):
    order = Order.query.get(id)
    if order.customer_id != user_id: raise UnauthorizedAccess("You don't have permission for resource")
    if not order: raise NotFoundError("Không tìm thấy đơn để cập nhật")
    return order


def find_all(**kwargs):
    orders = Order.query
    order_id = kwargs.get("order_id")
    status = kwargs.get('status')
    payment_method = kwargs.get('payment_method')
    sort_by = kwargs.get('sort_by')
    sort_dir = kwargs.get('sort_dir', "desc")
    order_type = kwargs.get("order_type")

    page = kwargs.get("page")

    start_date = kwargs.get("start_date")
    end_date = kwargs.get("end_date")

    if order_id:
        orders = orders.filter(Order.order_id == int(order_id))

    if order_type == "1":
        orders = orders.join(OnlineOrder)
        orders = orders.filter(Order.order_id == OnlineOrder.order_id)
    if order_type == "2":
        orders = orders.join(OfflineOrder)
        orders = orders.filter(Order.order_id == OfflineOrder.order_id)

    if status:
        status_array = [OrderStatus(int(status_elm)) for status_elm in status]
        orders = orders.filter(Order.status.in_(status_array))

    if payment_method:
        orders = orders.filter(Order.payment_method == PaymentMethod(int(payment_method)))

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        orders = orders.filter(Order.created_at >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        orders = orders.filter(Order.created_at <= end_date)

    orders = orders.order_by(desc(Order.created_at)) if sort_dir.__eq__("desc") else orders.order_by(
        asc(Order.created_at))

    page_size = app.config['ORDER_PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    total_page = math.ceil(orders.count() / page_size)
    orders = orders.slice(start, end)

    orders = [{
        **(order.online_order.to_dict() if order.online_order else order.offline_order.to_dict()),
        'total_amount': calculate_total_order_amount(order.order_id)
    }
        for order in orders.all()
    ]

    if 'total-amount' == sort_by:
        orders.sort(key=sort_by_total_amount, reverse=True if sort_dir.__eq__("desc") else False)

    return {
        'orders': orders,
        'total_page': total_page,
        'current_page': page
    }


def update_order(order_id, order_list):
    query = OrderDetail.query
    order = Order.query.get(order_id)

    allowed_status = [OrderStatus.DANG_XU_LY, OrderStatus.CHO_GIAO_HANG, OrderStatus.DANG_CHO_NHAN]
    if order.online_order is None and order.payment_method is not PaymentMethod.TIEN_MAT and order.status not in allowed_status:
        raise ConflictError("Điều kiện cập nhật đơn đơn không đáp ứng")

    order_details = query.filter(OrderDetail.order_id == order_id).all()

    for order_detail in order_details:
        order_detail.book.increase_book(order_detail.quantity)
        db.session.delete(order_detail)

    for order_item in order_list:
        book_id = order_item['book_id']

        book_db = Book.query.get(book_id)
        if book_db is None: raise NotFoundError('Không tìm thấy sách')

        quantity = int(order_item['quantity'])
        res = book_db.decrease_book(quantity=quantity)

        if not res:
            raise GeneralInsufficientError("Không đủ sách")

        price = order_item['price']
        order_detail = OrderDetail(order_id=order_id, book_id=book_id, quantity=quantity, price=price)
        db.session.add(order_detail)

    db.session.commit()


def create_online_order(user_id, request):
    payment_method = PaymentMethod.THE if request.get('paymentMethod').__eq__('VNPay') else PaymentMethod.TIEN_MAT
    status = OrderStatus.DANG_CHO_THANH_TOAN if request.get('paymentMethod').__eq__('VNPay') else OrderStatus.DANG_XU_LY
    shipping_method = ShippingMethod.GIAO_HANG if request.get('shippingMethod').__eq__(
        'ship') else ShippingMethod.CUA_HANG

    shipping_fee = request.get('shippingFee')
    online_order = OnlineOrder(status=status,
                               payment_method=payment_method,
                               created_at=datetime.now(),
                               address_id=request['addressId'],
                               shipping_method=shipping_method,
                               shipping_fee=shipping_fee,
                               customer_id=user_id
                               )

    for book in request['books']:
        book_db = Book.query.get(book['bookId'])
        if book_db is None: raise NotFoundError('Không tìm thấy sách')

        if not book_db.decrease_book(quantity=book['quantity']):
            raise InsufficientError(f"{book_db.title} không đủ số lượng", {
                'book_id': book_db.book_id,
                "current_quantity": book_db.quantity
            })

        order_detail = OrderDetail(book_id=book['bookId'], quantity=book['quantity'], price=book['finalPrice'])
        online_order.order_detail.append(order_detail)

    db.session.add(online_order)
    db.session.commit()
    return online_order


def create_offline_order(order_list, employee_id, user=None):
    offline_order = OfflineOrder(status=OrderStatus.DA_HOAN_THANH,
                                 payment_method=PaymentMethod.TIEN_MAT,
                                 created_at=datetime.utcnow() + timedelta(hours=7),
                                 address_id=1,
                                 employee_id=employee_id,
                                 customer=user)
    if user is not None:
        user.orders.append(offline_order)
    #

    total_amount = 0

    for order_item in order_list:
        book_id = order_item['book_id']
        book_db = Book.query.get(book_id)

        if book_db is None: raise NotFoundError('Không tìm thấy sách')

        quantity = int(order_item['quantity'])

        res = book_db.decrease_book(quantity=quantity)
        if not res:
            raise GeneralInsufficientError("Không đủ sách")
        price = int(order_item['price'])
        order_detail = OrderDetail(order_id=offline_order.order_id, book_id=book_id, quantity=quantity, price=price)
        offline_order.order_detail.append(order_detail)
        total_amount = total_amount + quantity * price

    payment_detail = PaymentDetail(order=offline_order, created_at=datetime.utcnow() + timedelta(hours=7),
                                   amount=total_amount)
    offline_order.payment_detail = payment_detail

    db.session.add(offline_order)
    db.session.commit()

    return offline_order.to_detail_dict()


def calculate_total_order_amount(order_id):
    total_amount = db.session.query(func.sum(OrderDetail.quantity * OrderDetail.price)).filter(
        OrderDetail.order_id == order_id).first()[0]

    shipping_fee = db.session.query(OnlineOrder.shipping_fee).filter(OnlineOrder.order_id == order_id).first()
    total_amount = total_amount + shipping_fee[0] if shipping_fee is not None else total_amount
    return Decimal(total_amount)


def delete_orders_after_48hrs():
    config = get_config()
    expired_time = datetime.utcnow() + timedelta(hours=7) - timedelta(seconds=config.order_cancel_period)
    orders = Order.query.filter(Order.created_at < expired_time,
                                Order.payment_method == PaymentMethod.TIEN_MAT,
                                Order.status == OrderStatus.DANG_CHO_NHAN)
    orders = orders.join(OnlineOrder).filter(Order.created_at < expired_time,
                                             Order.payment_method == PaymentMethod.TIEN_MAT,
                                             Order.status == OrderStatus.DANG_CHO_NHAN,
                                             OnlineOrder.shipping_method == ShippingMethod.CUA_HANG).all()

    for order in orders:
        create_order_cancellation({
            "orderId": order.order_id,
            "reason": "Đơn quá 48h"
        })


def delete_payment_after_48hrs():
    print("ok")
    expired_time = datetime.utcnow() + timedelta(hours=7) - timedelta(hours=48)
    orders = Order.query.filter(Order.created_at < expired_time,
                                Order.payment_method == PaymentMethod.THE,
                                Order.status == OrderStatus.DANG_CHO_THANH_TOAN)
    orders = orders.join(OnlineOrder).filter(Order.created_at < expired_time,
                                             Order.payment_method == PaymentMethod.THE,
                                             Order.status == OrderStatus.DANG_CHO_THANH_TOAN).all()

    for order in orders:
        create_order_cancellation({
            "orderId": order.order_id,
            "reason": "Đơn chưa thanh toán quá 48h"
        })


def count_order():
    return Order.query.count()


def sort_by_total_amount(order):
    return order['total_amount']
