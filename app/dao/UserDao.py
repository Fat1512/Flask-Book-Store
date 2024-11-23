import app.model.User
from app.model.User import User
import hashlib
from app import db
import cloudinary.uploader
from app.model.User import UserRole

def auth_user(username, password, role=UserRole.USER):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password),
                             User.user_role.__eq__(role)).first()

def add_user(first_name, last_name, username, password,email,avt_url, sex=None,  phone_number=None, date_of_birth=None,  isActive=None, last_access=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(first_name=first_name, last_name=last_name, username=username,password=password, email=email, avt_url='https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg', sex=sex,phone_number=phone_number, date_of_birth=date_of_birth, isActive=isActive, last_access=last_access)
    if not avt_url:
        avt_url = 'https://png.pngtree.com/png-vector/20191101/ourmid/pngtree-cartoon-color-simple-male-avatar-png-image_1934459.jpg'
    if avt_url:
        res = cloudinary.uploader.upload(avt_url)
        u.avt_url = res.get('secure_url')

    db.session.add(u)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)
