import hashlib
import hmac
import math
import random
import time
import uuid
from datetime import timedelta, datetime
from urllib.parse import urlencode
from flask import request, redirect, url_for

from app import app


def generate_vnp_txn_ref():
    # Use the current timestamp for uniqueness
    timestamp = int(time.time())  # Current time in seconds since epoch

    # Generate a random UUID and extract the first 8 characters
    random_part = uuid.uuid4().hex[:8]

    # Combine timestamp and random part to form the TxnRef
    txn_ref = f"{timestamp}{random_part}"
    return txn_ref


def get_client_ip():
    # Check if the request has the X-Forwarded-For header (common when behind a proxy)
    if 'X-Forwarded-For' in request.headers:
        # The header can contain multiple IPs, so we take the first one
        return request.headers.getlist('X-Forwarded-For')[0]
    else:
        # Fallback to remote address if the header is not present
        return request.remote_addr


def generate_vnpay_url(order):
    vnpay_url = app.config["VNPAY_URL"]
    vnpay_data = {
        'vnp_Version': '2.1.0',
        'vnp_TmnCode': app.config["VNPAY_TMN_CODE"],
        'vnp_BankCode': "NCB",
        'vnp_Amount': math.ceil(order.get_amount() * 100),  # Amount in the smallest currency unit (e.g., cent)
        'vnp_Command': 'pay',
        'vnp_OrderInfo': f"Thanh toan don hang {order.order_id}",
        'vnp_OrderType': "Thanh toan don hang",
        'vnp_CurrCode': "VND",
        'vnp_Locale': 'vn',
        'vnp_ReturnUrl': f"{app.config['VNPAY_RETURN_URL']}?orderId={order.order_id}",
        'vnp_TxnRef': generate_vnp_txn_ref(),
        'vnp_CreateDate': time.strftime('%Y%m%d%H%M%S', time.localtime()),
        'vnp_IpAddr': get_client_ip()

    }
    vnp_expire_date = (datetime.now() + timedelta(minutes=15)).strftime("%Y%m%d%H%M%S")
    vnpay_data["vnp_ExpireDate"] = vnp_expire_date
    print(vnpay_data['vnp_ReturnUrl'])
    sorted_data = sorted(vnpay_data.items())
    encoded_query = urlencode(sorted_data)
    encoded_query += f"&vnp_SecureHash={generate_secure_hash(encoded_query)}"
    vnpay_url += '?' + encoded_query
    return vnpay_url


def generate_secure_hash(encoded_query):
    return hmac.new(
        app.config['VNPAY_HASH_SECRET'].encode("utf-8"),  # Key
        encoded_query.encode("utf-8"),  # Message
        hashlib.sha512  # Hash function
    ).hexdigest()


def validate_vnpay_response(response_data):
    secure_hash = response_data.pop('vnp_SecureHash')
    data_string = '&'.join([f"{key}={value}" for key, value in response_data.items()])
    data_string += f"&{app.config['VNPAY_HASH_SECRET']}"

    expected_hash = hashlib.sha256(data_string.encode('utf-8')).hexdigest().upper()

    return secure_hash == expected_hash
