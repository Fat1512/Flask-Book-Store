from sqlalchemy import Column, Integer, String, ForeignKey, Double, DATETIME
from app import db, app
from sqlalchemy.orm import relationship
from app.model.BookImage import BookImage
from app.model.BookGerne import BookGerne
from app.model.Publisher import Publisher
from app.model.ExtendedBook import ExtendedBook
from app.model.Comment import Comment

from app.model.CartItem import CartItem
from app.model.Cart import Cart
from app.model.FormImportDetail import FormImportDetail


class Book(db.Model):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer, default=0)
    price = Column(Double)
    description = Column(String)
    release_date = Column(DATETIME)
    num_page = Column(Integer)
    dimension = Column(String)
    weight = Column(Double)
    barcode = Column(String)
    format = Column(String)
    publisher_id = Column(Integer, ForeignKey('publisher.publisher_id'), nullable=False)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))

    book_gerne = db.relationship('BookGerne', back_populates='books', lazy=True)
    publisher_info = db.relationship('Publisher', back_populates='publisher_books_relation',
                                     foreign_keys=[publisher_id], lazy=True)
    images = db.relationship('BookImage', backref='book', lazy=True)
    order_detail = relationship("OrderDetail", back_populates="book", lazy=True)
    form_import_detail = relationship("FormImportDetail", back_populates="book", lazy=True)

    extended_books = db.relationship('ExtendedBook', back_populates='book', lazy=True)
    cart_item = db.relationship('CartItem', back_populates='book', lazy=True)

    def to_dict(self):
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
            "images": [image.to_dict() for image in self.images],
            'format': self.format,
            "publisher": "Kim đồng",
            'book_gerne': self.book_gerne.to_dict(),
            'extended_books': [extended for extended in self.extended_books],
        }

    def to_dto(self):
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
            'format': self.format,
            "publisher": "Kim đồng",
            'book_gerne': self.book_gerne.to_dto(),
            'book_image': [image.to_dto() for image in self.images],
            'extended_books': [extended.to_dto() for extended in self.extended_books],
        }

    def to_dict_manage(self):
        json = self.to_dict()
        json['gerne'] = {
            'id': self.book_gerne_id,
            'name': self.book_gerne.name
        }
        return json

    def __str__(self):
        pass

    def increase_book(self, quantity):
        self.quantity += quantity

    def decrease_book(self, quantity):
        if self.quantity < quantity:
            return False
        self.quantity -= quantity
