import pdb

import app.model.User
from app.exception.NotFoundError import NotFoundError
from app.exception.BadRequestError import BadRequestError
from app.model.Address import Address
from app.model.Cart import Cart
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
import validators


def auth_user(identifier, password, role=None):
    # Mã hóa password
    password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()

    if not identifier or not password:
        return None

    # Kiểm tra nếu identifier là email hay username
    query = Account.query.options(joinedload(Account.user)).filter(
        (Account.username == identifier.strip()) | (Account.user.has(email=identifier.strip())),
        # Truy vấn email qua mối quan hệ với User
        Account.password == password
    )

    if role:
        query = query.filter(Account.user.has(user_role=role))

    account = query.first()

    # Trả về User nếu Account tồn tại
    return account.user if account else None


# def auth_user(username, password, role=UserRole.USER):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#     return User.query.filter(User.username.__eq__(username.strip()),
#                              User.password.__eq__(password),
#                              User.user_role.__eq__(role)).first()

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
    return {
        'id': u.user_id,
        'fullname': u.full_name
    }


def add_user(first_name, last_name, username, password, email, phone_number, avt_url=None, sex=None,
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
    u.cart = Cart(user=u)
    db.session.add(u)
    db.session.flush()  # Flush để có user_id

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
    user = User.query
    user = user.filter(User.user_id == user_id, User.phone_number == phone_number).first()

    if not user:
        raise BadRequestError("Không tồn tại user với số điện thoại tương ứng")

    return user


def find_user_address(user_id):
    return Address.query.filter_by(user_id=user_id, is_active=True).all()


def add_address(user_id, data):
    user = User.query.get(user_id)
    address_db = Address(first_name=data['first_name'], last_name=data['last_name'],
                         phone_number=data['phone'],
                         city=data['city'],
                         district=data['district'],
                         ward=data['ward'],
                         address=data['address'], )
    user.address.append(address_db)
    db.session.commit()

    return address_db


def delete_address(user_id, address_id):
    user = User.query.get(user_id)

    for a in user.address:
        if a.address_id == address_id:
            a.is_active = False
            db.session.commit()
            return a

    raise NotFoundError("Not found address")


def update_address(user_id, address_id, data):
    user = User.query.get(user_id)
    for a in user.address:
        if a.address_id == address_id:
            for key, value in data.items():
                if hasattr(a, key):  # Optional: Check if the attribute exists
                    setattr(a, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
                    # Commit the changes
            db.session.commit()
            return a
    raise NotFoundError("Not found address")


def find_by_phone_number(phone_number):
    query = User.query
    query = query.filter(User.phone_number == phone_number)
    return query.first()


def find_customer_phone_number(phone_number):
    obj = [{
        'id': item[0],
        'fullname': item[1] + " " + item[2],
        'phone_number': item[3]
    }
        for item in db.session.execute(
            select(User.user_id, User.first_name, User.last_name, User.phone_number).where(
                User.phone_number.contains(phone_number)))
    ]
    return obj


def check_exists(username=None, email=None, phone_number=None):
    if username and Account.query.filter_by(username=username).first():
        return True

    if email and User.query.filter_by(email=email).first():
        return True

    if phone_number and User.query.filter_by(phone_number=phone_number).first():
        return True

    return False


def check_exists_email(email=None):
    if email and User.query.filter_by(email=email).first():
        return True
    return False


# def get_user_by_id(user_id):
#     return User.query.get(user_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)
    # return User.query.options(joinedload(User.account)).filter_by(user_id=user_id).first()


def get_account_by_id(account_id):
    return Account.query.get(account_id)


def get_user_by_email(email):
    return db.session.query(User).filter_by(email=email).first()


def is_valid_email(email):
    return validators.email(email)


def update_password(username, password):
    hashed_password = hashlib.md5(password.strip().encode('utf-8')).hexdigest()
    account = db.session.query(Account).options(joinedload(Account.user)).filter_by(username=username.strip()).first()
    if account:
        account.password = hashed_password
        db.session.commit()
