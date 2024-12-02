from app.model.Book import Book
from app import app, db
from app.model.BookGerne import BookGerne
from app.model.Book import Book
import math


def find_by_id(id):
    return Book.query.get(id)


def increase_book_quantity(id, quantity):
    book = Book.query.get(id)
    book.quantity = book.quantity + quantity
    db.session.commit()


def find_by_barcode(barcode):
    book = Book.query
    book = book.filter(Book.barcode == barcode)
    return book.first()


def find_by_gerne(gerne_id):
    query = Book.query
    gerne = BookGerne.query.get(gerne_id)
    query = query.join(BookGerne)
    query = query.filter(BookGerne.lft.between(gerne.lft, gerne.rgt))
    return query.all()


def find_all(page=1):
    return Book.query.all()


def paginate_book(page=1,limit=app.config['PAGE_SIZE']):
    page_size = limit
    start = (page - 1) * page_size
    end = start + page_size
    total = Book.query.count()
    total_page = math.ceil(total / page_size)
    books = Book.query.slice(start, end).all()

    return {
        'total_book': total,
        'current_page': page,
        'pages': total_page,
        'books': books
    }


def find_by_barcode(barcode):
    return Book.query.filter(Book.barcode.__eq__(barcode))



def countBook():
    return Book.query.count()
