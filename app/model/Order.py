from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DATETIME, Double
from app import db, app
from app.model import Book
from enum import Enum as PythonEnum


class OrderStatus(PythonEnum):
    DANG_XU_LY = 1
    CHO_GIAO_HANG = 2
    DANG_GIAO_HANG = 3
    DA_HOAN_THANH = 4


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
    order_detail = relationship("OrderDetail", backref='order', lazy=True)
    online_order = relationship('OnlineOrder', backref='order', lazy=True, uselist=False)
    offline_order = relationship('OfflineOrder', backref='order', lazy=True, uselist=False)
    payment_detail = relationship('PaymentDetail', backref='order', lazy=True, uselist=False)

    def to_dict(self):
        json = {
            'order_id': self.order_id,
            'status': self.status.value,
            'payment_method': self.payment_method.value,
            'created_at': self.created_at,
            'order_detail': [order_detail.to_dict() for order_detail in self.order_detail]
        }
        if self.online_order:
            json['type'] = 1
            json.update(self.online_order.to_dict())
        else:
            json['type'] = 0
            json.update(self.offline_order.to_dict())

        if self.payment_detail:
            json['payment_detail'] = self.payment_detail.to_dict()
        return json

class OfflineOrder(db.Model):
    __tablename__ = 'offline_order'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)


class OnlineOrder(db.Model):
    __tablename__ = 'online_order'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    shipping_method = Column(Enum(ShippingMethod))
    shipping_fee = Column(Double)
    def to_dict(self):
        return {
            'shipping_method': self.shipping_method.value,
            'shipping_fee': self.shipping_fee
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

