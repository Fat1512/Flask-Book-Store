from sqlalchemy import Column, Integer, String, Boolean, Text, Date, DateTime, Enum
from app import db
from enum import Enum as RoleEnum
from datetime import datetime

class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2

class User(db.Model):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    sex = Column(Boolean, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone_number = Column(String(10))
    date_of_birth = Column(Date)
    avt_url = Column(Text, default="https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg")
    isActive = Column(Boolean, default=True)
    last_access = Column(DateTime, default=datetime.utcnow)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return self.isActive

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)