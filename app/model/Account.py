from sqlalchemy import Column, Integer, String, Boolean, Text, Date, DateTime, Enum, ForeignKey
from app import db, app
from sqlalchemy.orm import relationship
from enum import Enum as RoleEnum
from datetime import datetime
import hashlib
from app.model.Cart import Cart


class Account(db.Model):
    __tablename__ = 'account'
    account_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)

    user_id = Column(Integer, ForeignKey('user.user_id'))
    user = relationship("User", back_populates="account")

