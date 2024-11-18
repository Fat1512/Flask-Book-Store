from datetime import datetime

from main import db

class ImageOfBook(db.Model):
    __tablename__ = 'image_of_book'
    image_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    created_at = db.Column(db.DateTime)
    image_url = db.Column(db.String(255), unique=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
