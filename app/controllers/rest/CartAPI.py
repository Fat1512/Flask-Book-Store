from flask import Blueprint, jsonify, request

from app.dao.CartDao import find_by_user_id, update_cart as update, delete_cart_item, add_cart_item as add, \
    add_multiple_cart_item

cart_rest_bp = Blueprint('cart_rest', __name__)


@cart_rest_bp.route('/', methods=['POST'])
def increase_cart_item():
    pass


@cart_rest_bp.route('/', methods=['GET'])
def get_cart():
    cart = find_by_user_id(2)
    return cart.to_dict()


@cart_rest_bp.route('/', methods=['PUT'])
def update_cart():
    request_data = request.json
    cart_item = update(request_data)
    return jsonify({
        "status": 200,
        "message": "Update cart successfully",
        'data': cart_item.to_dict()
    })


@cart_rest_bp.route('/<int:bookId>', methods=['DELETE'])
def delete_cart(bookId):
    cart = delete_cart_item(bookId)
    print('test', cart)
    return jsonify({
        "status": 200,
        "message": "Delete cart item successfully",
        'currentItem': len(cart.cart_items) if len(cart.cart_items) else 0
    })


@cart_rest_bp.route('/<int:bookId>', methods=['POST'])
def add_cart_items(bookId):
    add(bookId)

    return jsonify({
        "status": 200,
        "message": "Add cart item successfully"
    })


@cart_rest_bp.route('/books', methods=['POST'])
def add_cart_item():
    request_data = request.json
    add_multiple_cart_item(request_data)
    return jsonify({
        "status": 200,
        "message": "Add cart item successfully"
    })
