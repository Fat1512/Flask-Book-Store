from flask import Blueprint, render_template

from app.dao.CartDao import find_by_user_id

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
def cart():
    cart = find_by_user_id(2)
    print(cart)
    return render_template("cart.html", cart=cart)


@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout-cart.html')
