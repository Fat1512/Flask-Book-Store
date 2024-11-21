from app.model.Order import Order
from sqlalchemy import desc, asc

#find by id, find by sdt khach hang
#filter by status, PTTT
#sort by thoi gian dat, tong tien

def find_by_id(id):
    return Order.query.get(id)


def find_all(**kwargs):
    orders = Order.query
    status = kwargs.get('status')
    payment_method = kwargs.get('paymentMethod')
    sortBy = kwargs.get('sortBy')
    sortDir = kwargs.get('dir')

    if status:
        orders = orders.filter(Order.status.value.__eq__(int(status)))

    if payment_method:
        orders = orders.filter(Order.payment_method.value.__eq__(int(payment_method)))

    if sortBy.__eq__('date'):
        orders = orders.order_by(desc(Order.created_at))

