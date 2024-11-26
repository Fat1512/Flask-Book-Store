from flask import Blueprint, render_template

from app.dao.CartDao import find_by_user_id

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
def cart():
    cart = find_by_user_id(2)
    cart_items = cart.cart_items
    total_price = cart.total_price()
    return render_template("cart.html", cart=cart, cart_items=cart_items, total_price=total_price)


@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout-cart.html')
