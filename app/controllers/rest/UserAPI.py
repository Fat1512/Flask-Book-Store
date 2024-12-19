from app.dao.UserDao import *
from flask import Blueprint, jsonify
from app.exception.AlreadyExistedError import AlreadyExistedError
from flask import render_template, request
import json

user_api_bp = Blueprint('/api/v1/user', __name__)


@user_api_bp.route("/phone_number/<phone_number>")
def get_customer_phone_number(phone_number):
    phone_number_info = find_customer_phone_number(phone_number)
    return jsonify({
        "message": "Success",
        "status": 200,
        "data": phone_number_info
    })


@user_api_bp.route("/phone_number/<phone_number>", methods=["POST"])
def create_customer_phone_number(phone_number):
    user = find_by_phone_number(phone_number)
    if user:
        raise AlreadyExistedError("Số điện thoại đã được đăng ký")

    user = add_offline_user("Default", "Default", "Default2", avt_url=None, sex=True,
                        phone_number=str(phone_number), isActive=True)
    user['phone_number'] = phone_number
    return {
        "message": "Tạo thành công",
        "status": 200,
        "data": user
    }