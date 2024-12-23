from datetime import datetime, timedelta

from app import db
from app.dao.OrderDAO import create_order_cancellation
from app.model.Order import Order, PaymentMethod, OrderStatus, OnlineOrder


def create_payment(payment):
    db.session.add(payment)
    db.session.commit()

