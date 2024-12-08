from app.elasticsearch.BookIndexService import delete_document, create_document
from app.exception.NotFoundError import NotFoundError
from app.model.Book import Book


def create(book_id):
    book = Book.query.get(book_id)
    if book is None: raise NotFoundError("Khong tim thay sach")

    book_document = book.to_dto()
    create_document(book_document)

def update_image():
    pass

def update_attribute_value():
    pass

def update_attribute():
    pass

def update_book_gerne():
    pass

def delete(book_id):
    book = Book.query.get(book_id)
    if book is None: raise NotFoundError("Khong tim thay sach")

    delete_document(book.book_id)


