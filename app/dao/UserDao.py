import app.model.User
from app.model.User import User
from app.model.Account import Account
import hashlib
from app import db
import cloudinary.uploader
from app.model.User import UserRole
import json
from app.model.Account import Account
from app.model.User import User
from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload



def auth_user(username, password, role=None):
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    if not username or not password:
        return None

    # Truy vấn từ Account và sử dụng quan hệ để lấy User
    query = Account.query.options(joinedload(Account.user)).filter(
        Account.username == username.strip(),
        Account.password == password
    )

    if role:
        query = query.filter(Account.user.has(user_role=role))

    account = query.first()

    # Trả về User nếu Account tồn tại
    return account.user if account else None



# def auth_user(username, password, role=UserRole.USER):
#     password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
#
#     if not username or not password:
#         return None
#
#     # Truy vấn từ Account và sử dụng quan hệ để lấy User
#     account = Account.query.options(joinedload(Account.user)).filter(
#         Account.username == username.strip(),
#         Account.password == password,
#         or_(
#             Account.user.has(user_role=role),
#             Account.user.has(user_role=UserRole.ADMIN)
#         )
#     ).first()
#
#     # Trả về User nếu Account tồn tại
#     return account.user if account else None


def add_offline_user(first_name, last_name, email, avt_url=None, sex=None, phone_number=None, date_of_birth=None,
                     isActive=None, last_access=None):
    u = User(first_name=first_name, last_name=last_name, email=email,
             avt_url='https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg',
             sex=sex, phone_number=phone_number, date_of_birth=date_of_birth, isActive=isActive,
             last_access=last_access)
    if not avt_url:
        avt_url = 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg'
    if avt_url:
        res = cloudinary.uploader.upload(avt_url)
        u.avt_url = res.get('secure_url')
    db.session.add(u)
    db.session.commit()


def add_user(first_name, last_name, username, password, email, avt_url=None, sex=None, phone_number=None,
             date_of_birth=None, isActive=None, last_access=None):
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


def add_employee(first_name, last_name, username, password, email, avt_url=None, sex=None, phone_number=None,
             date_of_birth=None, isActive=None, last_access=None, user_role=None):
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
        last_access=last_access,
        user_role=user_role  # Thêm user_role vào đây
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


def find_by_customer_id_phone_number(user_id, phone_number):
    query = User.query
    query = query.filter(User.user_id == user_id, User.phone_number == phone_number)
    return query.first()


def find_by_phone_number(phone_number):
    query = User.query
    query = query.filter(User.phone_number == phone_number)
    return query.first()


def find_customer_phone_number(phone_number):
    obj = [{
        'id': item[0],
        'name': item[1],
        'phone_number': item[2]
    }
        for item in db.session.execute(
            select(User.user_id, User.first_name, User.phone_number).where(User.phone_number.contains(phone_number)))
    ]

    return obj


def check_exists(username=None, email=None):
    if username and Account.query.filter_by(username=username).first():
        return True

    if email and User.query.filter_by(email=email).first():
        return True

    return False

# def get_user_by_id(user_id):
#     return User.query.get(user_id)


def get_user_by_id(user_id):
    return User.query.options(joinedload(User.account)).filter_by(user_id=user_id).first()


def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()


def update_password(username, password):
    hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    account = db.session.query(Account).options(joinedload(Account.user)).filter_by(username=username.strip()).first()
    if account:
        account.password = hashed_password
        db.session.commit()

