from app.model.Order import Order, PaymentDetail
from sqlalchemy import desc, asc, or_
from app import app
from app.model.Order import OrderStatus, PaymentMethod, OnlineOrder, OfflineOrder
import math


# find by id, find by sdt khach hang
# filter by status, PTTT
# sort by thoi gian dat, tong tien

def find_by_id(id):
    return Order.query.get(id)


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
        orders = orders.order_by(Order.created_at.desc()) if sort_dir.__eq__("desc") else orders.order_by(
            Order.created_at.asc())

    orders = [order.to_dict() for order in orders.all()]

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


def count_order():
    return Order.query.count()


def sort_by_total_amount(order):
    return order['total_amount']
