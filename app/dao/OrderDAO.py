from app.model.Order import Order, PaymentDetail
from sqlalchemy import desc, asc, or_
from datetime import datetime
from app import app, db
from app.model.Order import OrderStatus, PaymentMethod, OnlineOrder, OfflineOrder, OrderDetail
import math


# find by id, find by sdt khach hang
# filter by status, PTTT
# sort by thoi gian dat, tong tien

def find_by_id(id):
    order = Order.query.get(id)
    return order.online_order.to_dict() if order.online_order else order.offline_order.to_dict()



def find_all(**kwargs):
    orders = Order.query
    status = kwargs.get('status')
    payment_method = kwargs.get('payment_method')
    sort_by = kwargs.get('sort_by')
    sort_dir = kwargs.get('sort_dir', "desc")
    order_type = kwargs.get("order_type")

    page = kwargs.get("page")

    if order_type == "1":
        orders = orders.join(OnlineOrder)
        orders = orders.filter(Order.order_id == OnlineOrder.order_id)
    if order_type == "2":
        orders = orders.join(OfflineOrder)
        orders = orders.filter(Order.order_id == OfflineOrder.order_id)

    if status:
        orders = orders.filter(Order.status == OrderStatus(int(status)))

    if payment_method:
        orders = orders.filter(Order.payment_method == PaymentMethod(int(payment_method)))

    if 'date' == sort_by:
        orders = orders.order_by(desc(Order.created_at)) if sort_dir.__eq__("desc") else orders.order_by(
            asc(Order.created_at))

    # orders = [order.to_dict() for order in orders.all()]
    orders = [order.online_order.to_dict() if order.online_order else order.offline_order.to_dict() for order in orders.all()]

    if 'total-amount' == sort_by:
        orders.sort(key=sort_by_total_amount, reverse=True if sort_dir.__eq__("desc") else False)

    page_size = app.config['ORDER_PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    total_page = math.ceil(len(orders) / page_size)

    orders = orders[start: end]

    return {
        'orders': orders,
        'total_page': total_page,
        'current_page': page
    }


def update_order(order_id, order_list):
    query = OrderDetail.query
    query.filter(OrderDetail.order_id == order_id).delete()

    for order_item in order_list:
        book_id = order_item['book_id']
        quantity = order_item['quantity']
        price = order_item['price']
        order_detail = OrderDetail(order_id=order_id, book_id=book_id, quantity=quantity, price=price)
        db.session.add(order_detail)

    db.session.commit()


def create_offline_order(order_list):

    offline_order = OfflineOrder(status=OrderStatus.DA_HOAN_THANH,
                                 payment_method=PaymentMethod.TIEN_MAT,
                                 created_at=datetime.utcnow(),
                                 address_id=1,
                                 employee_id=2)

    db.session.add(offline_order)
    db.session.flush()

    order_detail_list = []
    total_amount = 0
    for order_item in order_list:
        book_id = order_item['book_id']
        quantity = int(order_item['quantity'])
        price = int(order_item['price'])
        order_detail = OrderDetail(order_id=offline_order.order_id, book_id=book_id, quantity=quantity, price=price)
        order_detail_list.append(order_detail)
        total_amount = total_amount + quantity * price

    payment_detail = PaymentDetail(order_id=offline_order.order_id, created_at=datetime.utcnow(), amount=total_amount)

    db.session.add_all(order_detail_list)
    db.session.add(payment_detail)
    db.session.commit()
    return offline_order.to_dict()

def count_order():
    return Order.query.count()


def sort_by_total_amount(order):
    return order['total_amount']
