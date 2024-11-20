from app import db


class BookGerne(db.Model):
    __tablename__ = 'book_gerne'
    book_gerne_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    lft = db.Column(db.Integer)
    rgt = db.Column(db.Integer)

    books = db.relationship('Book', backref='book_gerne', lazy=True)

    def __init__(self, book_type_id,name, description, lft, rgt):
        self.book_type_id = book_type_id
        self.name = name
        self.description = description
        self.lft = lft
        self.rgt = rgt

    def to_dict(self):
        books = []
        for book in self.books:
            books.append(book.to_dict())
        return {
            'book_type_id': self.book_type_id,
            'name': self.name,

            "books": books
        }
