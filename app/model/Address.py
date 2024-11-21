from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DATETIME, Double
from app import db, app
from app.model import Book
from enum import Enum as PythonEnum

class Address(db.Model):
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column('firstName', String, nullable=False)
    last_name = Column('lastName', String, nullable=False)
    phone_number = Column('phoneNumber', String)
    city = Column(String)
    country = Column(String)
    address = Column(String)

    user_id = Column(Integer, ForeignKey('user.user_id'))
    order = relationship("Order", back_populates="address")
    def to_dict(self):
        return {
            'address_id': self.address_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'city': self.city,
            'country': self.country,
            'address': self.address
        }