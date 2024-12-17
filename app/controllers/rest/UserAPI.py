from app.dao.UserDao import *
from flask import Blueprint, jsonify

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
