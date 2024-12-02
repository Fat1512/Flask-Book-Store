from sqlalchemy.testing.config import db_url
from app import db
from app.model.Cart import Cart
from app.model.CartItem import CartItem


def find_by_user_id(user_id):
    return Cart.query.filter(Cart.user_id == user_id).first()


def find_by_cart_id(cart_id):
    return Cart.query.get(cart_id)


def update_cart(request):
    cart = Cart.query.filter(Cart.cart_id == request.get('cartId')).first()
    respone = None
    for cart_item in request.get('cartItems'):
        for item in cart.cart_items:
            if item.book_id == int(cart_item.get('bookId')):
                if item.book.quantity < int(cart_item.get('quantity')):
                    return None
                item.quantity = int(cart_item.get('quantity'))
                respone = item

    db.session.commit()
    return respone


def delete_cart_item(book_id):
    cart = Cart.query.filter(Cart.cart_id == 2).first()
    for item in cart.cart_items:
        if item.book_id == book_id:
            cart.cart_items.remove(item)
    db.session.commit()

    return cart


def add_cart_item(book_id):
    cart = Cart.query.filter(Cart.cart_id == 2).first()
    for item in cart.cart_items:
        if item.book_id == book_id:
            item.quantity += 1
            db.session.commit()
            return

    cart_item = CartItem(book_id=book_id, cart_id=cart.cart_id, quantity=1)
    cart.cart_items.append(cart_item)
    db.session.commit()


def add_multiple_cart_item(books):
    cart = Cart.query.filter(Cart.cart_id == 2).first()
    for book in books:
        is_present = False
        for item in cart.cart_items:
            if item.book_id == book:
                item.quantity += 1
                is_present = True
        if not is_present:
            cart_item = CartItem(book_id=book, cart_id=cart.cart_id, quantity=1)
            cart.cart_items.append(cart_item)

    db.session.commit()
