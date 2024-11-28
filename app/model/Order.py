from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DATETIME, Double
from app import db, app
from app.utils.helper import *
import functools
from app.model import Book, User, Address
from enum import Enum as PythonEnum


# TYPE = 1 => OnlineOrder
# TYPE = 2 => OfflineOrder

class OrderStatus(PythonEnum):
    DANG_XU_LY = 1
    CHO_GIAO_HANG = 2
    DANG_GIAO_HANG = 3
    DA_HOAN_THANH = 4
    DA_HUY = 5


class PaymentMethod(PythonEnum):
    THE = 1
    TIEN_MAT = 2


class ShippingMethod(PythonEnum):
    GIAO_HANG = 1
    CUA_HANG = 2


class Order(db.Model):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.DANG_XU_LY)
    payment_method = Column(Enum(PaymentMethod))
    created_at = Column(DATETIME)

    address_id = Column(Integer, ForeignKey('address.address_id'))
    address = relationship("Address", back_populates="order")

    order_detail = relationship("OrderDetail", backref='order', lazy=True, cascade="all")
    online_order = relationship('OnlineOrder', backref='order', lazy=True, uselist=False, cascade="all")
    offline_order = relationship('OfflineOrder', backref='order', lazy=True, uselist=False, cascade="all")
    payment_detail = relationship('PaymentDetail', backref='order', lazy=True, uselist=False, cascade="all")

    def to_dict(self):
        json = {
            'order_id': self.order_id,
            'status': {
                'id': self.status.value,
                'name': ORDER_STATUS_TEXT[self.status.value - 1],
            },
            'payment': {
                'payment_method': {
                    'id': self.payment_method.value,
                    'name': PAYMENT_METHOD_TEXT[self.payment_method.value - 1]
                }
            },
            'created_at': self.created_at,
            'order_detail': [order_detail.to_dict() for order_detail in self.order_detail],
            'address': self.address.to_dict()
        }
        total_amount = 0
        for order_detail in [order_detail.to_dict() for order_detail in self.order_detail]:
            total_amount = total_amount + order_detail['price'] * order_detail['quantity']
        json['total_amount'] = total_amount

        if self.payment_detail:
            json['payment']['payment_detail'] = self.payment_detail.to_dict()

        return json


class OfflineOrder(Order):
    __tablename__ = 'offline_order'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)

    employee_id = Column(Integer, ForeignKey('user.user_id'))
    employee = relationship("User", back_populates="offline_orders")

    def to_dict(self):
        json = super().to_dict()
        json['order_type'] = {
            'id': 2,
            'name': ORDER_TYPE_TEXT[1],
            'detail': {
                'employee_name': self.employee.first_name + ' ' + self.employee.last_name
            }
        }
        return json


class OnlineOrder(Order):
    __tablename__ = 'online_order'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    shipping_method = Column(Enum(ShippingMethod))
    shipping_fee = Column(Double)
    note = Column(String)

    customer_id = Column(Integer, ForeignKey('user.user_id'))
    customer = relationship("User", back_populates="online_orders")
    order_cancellation = relationship('OrderCancellation', backref='online_order', lazy=True, uselist=False)

    def to_dict(self):
        json = super().to_dict()
        json['order_type'] = {
            'id': 1,
            'name': ORDER_TYPE_TEXT[0],
            'detail': {
                'shipping_method': {
                    'id': self.shipping_method.value,
                    'name': SHIPPING_METHOD_TEXT[self.shipping_method.value - 1]
                },
                'shipping_fee': self.shipping_fee,
                'note': self.note,
                'customer_id': self.customer_id
            }
        }
        json['total_amount'] = json['total_amount'] + json['order_type']['detail']['shipping_fee']
        return json


class OrderCancellation(db.Model):
    __tablename__ = 'order_cancellation'
    order_id = Column(Integer, ForeignKey('online_order.order_id'), primary_key=True)
    created_at = Column(DATETIME)
    reason = Column(String)

    def to_dict(self):
        return {
            'reason': self.reason,
            'created_at': self.created_at
        }


class OrderDetail(db.Model):
    __tablename__ = 'order_detail'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('book.book_id'), primary_key=True)
    book = relationship("Book", back_populates="order_detail")
    quantity = Column(Integer)
    price = Column(Double)

    def to_dict(self):
        return {
            'quantity': self.quantity,
            'price': self.price,
            'book': self.book.to_dict()
        }


class PaymentDetail(db.Model):
    __tablename__ = 'payment_detail'
    payment_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DATETIME)
    amount = Column(Double)

    order_id = Column(Integer, ForeignKey('order.order_id'), unique=True)

    def to_dict(self):
        return {
            'amount': self.amount,
            'created_at': self.created_at
        }
