from app.model.Order import Order, PaymentDetail
from sqlalchemy import desc, asc, func, or_
from datetime import datetime
from app import app, db
from app.model.Order import OrderStatus, PaymentMethod, OnlineOrder, OfflineOrder, OrderDetail
import math


# find by id, find by sdt khach hang
# filter by status, PTTT
# sort by thoi gian dat, tong tien

def find_by_id(order_id):
    order = Order.query.get(order_id)
    order = order.online_order.to_detail_dict() if order.online_order else order.offline_order.to_detail_dict()
    order['total_amount'] = calculate_total_order_amount(order_id)
    return order


def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    order.status = status
    db.session.commit()


def find_order_by_id(id):
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


def update_order_status(order_id, status):
    order = Order.query.get(order_id)
    order.status = status

    db.session.commit()


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


def create_online_order(request):
    payment_method = PaymentMethod.TIEN_MAT if request.get('paymentMethod').__eq__('inperson') else PaymentMethod.THE
    shipping_method = ShippingMethod.GIAO_HANG if request.get('shippingMethod').__eq__(
        'ship') else ShippingMethod.CUA_HANG
    shipping_fee = request.get('shippingFee')
    online_order = OnlineOrder(status=OrderStatus.DANG_XU_LY,
                               payment_method=payment_method,
                               created_at=datetime.utcnow(),
                               address_id=request['addressId'],
                               shipping_method=shipping_method,
                               shipping_fee=shipping_fee,
                               customer_id=2
                               )
    db.session.add(online_order)
    db.session.flush()

    # order_detail_list = []
    for book in request['books']:
        order_detail = OrderDetail(book_id=book['bookId'], quantity=book['quantity'], price=book['finalPrice'])
        online_order.order_detail.append(order_detail)

    db.session.commit()
    return online_order


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
    return offline_order.to_detail_dict()


def calculate_total_order_amount(order_id):
    total_amount = db.session.query(func.sum(OrderDetail.quantity * OrderDetail.price)).filter(OrderDetail.order_id == order_id).first()[0]
    shipping_fee = db.session.query(OnlineOrder.shipping_fee).filter(OnlineOrder.order_id == order_id).first()
    total_amount = total_amount + shipping_fee[0] if shipping_fee is not None else total_amount
    return total_amount

def count_order():
    return Order.query.count()


def sort_by_total_amount(order):
    return order['total_amount']
