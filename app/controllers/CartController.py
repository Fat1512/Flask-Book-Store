from flask import Blueprint, render_template

from app.dao import AddressDAO
from app.dao.CartDao import find_by_user_id, find_by_cart_id

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
def cart():
    cart = find_by_user_id(2)

    return render_template("cart.html", cart=cart)


@cart_bp.route('/checkout', methods=['GET'])
def checkout():
    address_default = AddressDAO.find_by_user_id(1)
    address_user = AddressDAO.find_by_user_id(2)

    return render_template('checkout-cart.html', address_default=address_default, address_user=address_user)
