from flask_login import current_user
from sqlalchemy.testing.config import db_url
from app import db
from app.dao.BookDAO import find_by_id
from app.exception.CartItemError import CartItemError
from app.exception.InsufficientError import InsufficientError
from app.exception.NotFoundError import NotFoundError
from app.model.Book import Book
from app.model.Cart import Cart
from app.model.CartItem import CartItem


def find_by_user_id(user_id):
    return Cart.query.filter(Cart.user_id == user_id).first()


def check_quantity(cart_items):
    cart_insufficient = []
    for cart_item in cart_items:
        book = find_by_id(cart_item.book_id)
        if not book:
            raise NotFoundError("Book not found")

        if cart_item.quantity > book.quantity:
            cart_item.quantity = book.quantity
            cart_insufficient.append({
                'book_id': book.book_id,
                'quantity': cart_item.quantity,
                'book_image': book.images[0].image_url if len(book.images) else None,
                'title': book.title,
                'price': book.price,
                'isInsufficient': True
            })
        else:
            cart_insufficient.append({
                'book_id': book.book_id,
                'quantity': cart_item.quantity,
                'book_image': book.images[0].image_url if len(book.images) else None,
                'title': book.title,
                'price': book.price,
                'isInsufficient': False
            })
    return cart_insufficient


def find_by_cart_id(cart_id):
    return Cart.query.get(cart_id)


def update_cart(user_id, cart_item):
    cart = Cart.query.filter(Cart.user_id == user_id).first()
    respone = None

    for item in cart.cart_items:
        if item.book_id == int(cart_item.get('bookId')):
            if item.book.quantity < int(cart_item.get('quantity')):
                raise CartItemError(f"{item.book.title} chỉ còn {item.book.quantity}")
            item.quantity = int(cart_item.get('quantity'))
            respone = item

    db.session.commit()
    return respone


def delete_cart_item(user_id, book_id):
    cart = Cart.query.filter(Cart.user_id == user_id).first()
    for item in cart.cart_items:
        if item.book_id == book_id:
            cart.cart_items.remove(item)
    db.session.commit()

    return cart


def add_cart_item(book_id):
    cart = Cart.query.filter(Cart.user_id == current_user.get_id()).first()
    book = Book.query.get(book_id)
    for item in cart.cart_items:
        if item.book_id == book_id:
            if item.book.quantity < (item.quantity + 1):
                raise CartItemError(f"{item.book.title} chỉ còn {item.book.quantity} sản phẩm")
            item.quantity += 1
            db.session.commit()
            return item

    cart_item = CartItem(book_id=book_id, cart_id=cart.cart_id, quantity=1)
    cart.cart_items.append(cart_item)
    db.session.commit()
    return cart_item


def add_multiple_cart_item(user_id, books):
    cart = find_by_user_id(user_id)
    for book_id in books:
        is_present = False
        book = find_by_id(book_id)
        if not book:
            raise NotFoundError("Book not found")
        if book.quantity < 1:
            raise CartItemError(f"{book.title} không còn đủ sản phẩm")
        for item in cart.cart_items:
            if item.book_id == book_id:
                if book.quantity <= item.quantity:
                    raise CartItemError(f"{book.title} không còn đủ sản phẩm")
                item.quantity += 1
                is_present = True
        if not is_present:
            cart_item = CartItem(book_id=book_id, cart_id=cart.cart_id, quantity=1)
            cart.cart_items.append(cart_item)

    db.session.commit()
