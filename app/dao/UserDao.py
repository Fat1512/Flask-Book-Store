import app.model.User
from app.model.User import User
from app.model.Account import Account
import hashlib
from app import db
import cloudinary.uploader
from app.model.User import UserRole

from sqlalchemy import or_
from sqlalchemy.orm import joinedload


def auth_user(username, password, role=UserRole.USER):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    # Truy vấn từ Account và sử dụng quan hệ để lấy User
    account = Account.query.options(joinedload(Account.user)).filter(
        Account.username == username.strip(),
        Account.password == password,
        or_(
            Account.user.has(user_role=role),
            Account.user.has(user_role=UserRole.ADMIN)
        )
    ).first()

    # Trả về User nếu Account tồn tại
    return account.user if account else None


# def auth_user(username, password, role=UserRole.USER):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#     return User.query.filter(User.username.__eq__(username.strip()),
#                              User.password.__eq__(password),
#                              User.user_role.__eq__(role)).first()

def add_user(first_name, last_name, username, password, email, avt_url=None, sex=None, phone_number=None, date_of_birth=None, isActive=None, last_access=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    # Tạo bản ghi User
    u = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        avt_url=avt_url or 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg',
        sex=sex,
        phone_number=phone_number,
        date_of_birth=date_of_birth,
        isActive=isActive,
        last_access=last_access
    )
    db.session.add(u)
    db.session.flush()  # Flush để có user_id

    # Tạo bản ghi Account
    account = Account(
        username=username,
        password=password,
        user_id=u.user_id
    )
    db.session.add(account)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.options(joinedload(User.account)).filter_by(user_id=user_id).first()

# def get_user_by_id(user_id):
#     return User.query.get(user_id)
