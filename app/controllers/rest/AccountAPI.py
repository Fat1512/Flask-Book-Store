from flask import Blueprint, request, jsonify

from app.dao.CommentDAO import create_comment, reply_comment
from app.dao.OrderDAO import find_add_by_user_id

account_rest_bp = Blueprint('account_rest', __name__)


@account_rest_bp.route('/purchase', methods=['GET'])
def get_purchase():
    status = request.args.get('status')
    orders = find_add_by_user_id(status)

    order_to_dict = [order.to_dict() for order in orders]
    return jsonify({
        "msg": "success",
        "status": 200,
        "orders": order_to_dict
    })


@account_rest_bp.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    reply_comment(data)
    return jsonify({
        "msg": "success",
        "status": 200,
    })


@account_rest_bp.route('/comment', methods=['POST'])
def post_comment():
    data = request.json

    create_comment(data)
    return jsonify({
        "msg": "success",
        "status": 200,
    })
