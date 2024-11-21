from app.model.Book import Book
from app import app
import math


def find_by_id(id):
    return Book.query.get(id)


def find_all(page=1):
    return Book.query.all()


def paginate_book(page=1):
    page_size = app.config['PAGE_SIZE']
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
