from sqlalchemy import Column, Integer, String, ForeignKey, Double
from app import db
from sqlalchemy.orm import relationship
from app.model.BookImage import ImageOfBook

class Book(db.Model):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer)
    price = Column(Double)
    description = Column(String)
    release_date = Column(String)
    num_page = Column(Integer)
    weight = Column(Double)
    barcode = Column(String)
    format = Column(String)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))
    images = db.relationship('ImageOfBook', backref='book', lazy=True)
    order_detail = relationship("OrderDetail", back_populates="book")

    def to_dict(self):
        images = []
        for image in self.images:
            images.append(image.to_dict())
        # Convert the set to a list here
        return {
            "book_id": self.book_id,
            "author": self.author,
            "title": self.title,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "book_gerne_id": self.book_gerne_id,
            "page_number": self.num_page,
            "weight": self.weight
        }

    def __str__(self):
        pass
