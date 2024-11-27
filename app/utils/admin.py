from app import db, app
from app.model.BookGerne import BookGerne
from app.model.Book import Book
from sqlalchemy.sql import func
from app.model.CartItem import CartItem


def book_gerne_statistic():
    return db.session.query(
        BookGerne.book_gerne_id,  # ID thể loại sách
        BookGerne.name,  # Tên thể loại sách
        func.sum(Book.price * CartItem.quantity).label('total_revenue')  # Tính doanh thu
    ).join(Book, BookGerne.book_gerne_id == Book.book_gerne_id, isouter=True  # Liên kết bảng book
           ).join(CartItem, Book.book_id == CartItem.book_id, isouter=True  # Liên kết bảng cart_item
                  ).group_by(BookGerne.book_gerne_id, BookGerne.name  # Nhóm theo thể loại
                             ).order_by(BookGerne.book_gerne_id, func.sum(Book.price * CartItem.quantity).desc()
                                        # Sắp xếp theo mã thể loại và doanh thu
                                        ).all()

    # return db.session.query(BookGerne.book_gerne_id, BookGerne.name, func.count(Book.book_id)) \
    #     .join(Book, BookGerne.book_gerne_id.__eq__(Book.book_gerne_id), isouter=True) \
    #     .group_by(BookGerne.book_gerne_id, BookGerne.name).all()


def total_revenue_per_gerne():
    # Truy vấn tổng doanh thu theo thể loại sách
    result = db.session.query(
        BookGerne.name.label('gerne_name'),  # Tên thể loại
        func.sum(Book.price * CartItem.quantity).label('total_revenue')  # Doanh thu
    ).join(Book, BookGerne.book_gerne_id == Book.book_gerne_id, isouter=True) \
        .join(CartItem, Book.book_id == CartItem.book_id, isouter=True) \
        .group_by(BookGerne.name)  # Nhóm theo thể loại sách

    # Tính tổng doanh thu của tất cả các thể loại
    total_revenue = sum(item.total_revenue if item.total_revenue is not None else 0 for item in result)

    return total_revenue


with app.app_context():
    stats = book_gerne_statistic()
    print(stats)


def get_books_by_gerne(gerne_id):
    return db.session.query(Book.book_id, Book.title, Book.quantity) \
        .filter(Book.book_gerne_id == gerne_id).all()


with app.app_context():
    stats = get_books_by_gerne(10)
    print(stats)
