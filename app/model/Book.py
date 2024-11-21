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
    # release_date = Column(DateTime)
    num_page = Column(Integer)
    book_gerne_id = Column(Integer, ForeignKey('book_gerne.book_gerne_id'))

    images = db.relationship('ImageOfBook', backref='book', lazy=True)

    def to_dict(self):
        images = []
        for image in self.images:
            images.append(image.to_dict())
        # Convert the set to a list here
        return {
            "book_id":self.book_id,
            "author": self.author,
            "title": self.title,
            "quantity": self.quantity,
            "price": self.price,
            "description": self.description,
            "book_gerne_id": self.book_gerne_id,
            "num_page": self.num_page,
            "weight": self.weight,
            "images": images,
        }

    def __str__(self):
        pass
