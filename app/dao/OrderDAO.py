from app.model.Order import Order, PaymentDetail
from sqlalchemy import desc, asc
from app import app


# find by id, find by sdt khach hang
# filter by status, PTTT
# sort by thoi gian dat, tong tien

def find_by_id(id):
    return Order.query.get(id)


def find_all(**kwargs):
    orders = Order.query
    status = kwargs.get('status')
    payment_method = kwargs.get('paymentMethod')
    sort_by = kwargs.get('sortBy')
    sort_dir = kwargs.get('dir', "DESC")
    page = kwargs.get("page")

    if status:
        orders = orders.filter(Order.status.value.__eq__(int(status)))

    if payment_method:
        orders = orders.filter(Order.payment_method.value.__eq__(int(payment_method)))

    if sort_by.__eq__('date'):
        orders = orders.order_by(desc(Order.created_at)) if sort_dir.__eq__("DESC") else orders.order_by(
            asc(Order.created_at))

    if sort_by.__eq__('total_amount'):
        orders = orders.join(Order.payment_detail)
        orders = orders.order_by(desc(PaymentDetail.amount)) if sort_dir.__eq__("DESC") \
            else orders.order_by(asc(PaymentDetail.amount))

    page_size = app.config['ORDER_PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    orders = orders.slice(start, end)

    return orders
