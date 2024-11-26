from app import db, app
from app.model.BookGerne import BookGerne
from app.model.Book import Book
from sqlalchemy.sql import func


def book_gerne_statistic():
    return db.session.query(BookGerne.book_gerne_id, BookGerne.name, func.count(Book.book_id)) \
        .join(Book, BookGerne.book_gerne_id.__eq__(Book.book_gerne_id), isouter=True) \
        .group_by(BookGerne.book_gerne_id, BookGerne.name).all()


with app.app_context():
    stats = book_gerne_statistic()
    print(stats)


def get_books_by_genre(genre_id):
    return db.session.query(Book.book_id, Book.title, Book.quantity) \
        .filter(Book.book_gerne_id == genre_id).all()

with app.app_context():
    stats = get_books_by_genre(10)
    print(stats)
