from sqlalchemy import Column, Integer, String, ForeignKey, Double
from app import db
from app.model.BookImage import ImageOfBook

class Book(db.Model):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    quantity = Column(Integer)
    price = Column(Double)
    description = Column(String)
    weight = Column(Double)
    num_page = Column(Integer)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))

    images = db.relationship('ImageOfBook', backref='book', lazy=True)

    def to_dict(self):
        # Convert the set to a list here
        return {
            "author": self.author,
            "name": self.name,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "book_type_id": self.book_type_id,
            "page_number": self.page_number,
            "weight": self.weight
        }

    def __str__(self):
        pass
