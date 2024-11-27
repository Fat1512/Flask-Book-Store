from sqlalchemy import Column, Integer, String, ForeignKey, Double, DATETIME
from app import db, app
from sqlalchemy.orm import relationship
from app.model.BookImage import ImageOfBook
from app.model.ExtendedBook import ExtendedBook
from app.model.Order import OrderDetail
from app.model.CartItem import CartItem
from app.model.Cart import Cart


class Book(db.Model):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer)
    price = Column(Double)
    description = Column(String)
    release_date = Column(DATETIME)
    num_page = Column(Integer)
    dimension = Column(String)
    weight = Column(Double)
    barcode = Column(String)
    format = Column(String)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))
    images = db.relationship('ImageOfBook', backref='book', lazy=True)
    order_detail = relationship("OrderDetail", back_populates="book")

    extended_books = db.relationship('ExtendedBook', back_populates='book', lazy=True)
    cart_item = db.relationship('CartItem', back_populates='book', lazy=True)

    def to_dict(self):
        images_dict = [image.to_dict() for image in self.images]
        extended_books_dict = [ex.to_dict() for ex in self.extended_books]
        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "book_gerne_id": self.book_gerne_id,
            "page_number": self.num_page,
            "weight": self.weight,
            "barcode": self.barcode,
            "images": images_dict,
            "extended_books": extended_books_dict,
        }

    def __str__(self):
        pass

    def increase_book(self, quantity):
        self.quantity += quantity

    def decrease_book(self, quantity):
        if self.quantity < quantity:
            return False
        self.quantity -= quantity
