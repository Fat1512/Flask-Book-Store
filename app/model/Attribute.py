from sqlalchemy import Integer, ForeignKey

from app import db
from app.model.ExtendedBook import ExtendedBook


class Attribute(db.Model):
    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name = db.Column(db.String(50), unique=True, nullable=False)
    book_gerne_id = db.Column(Integer, ForeignKey('book_gerne.book_gerne_id'))

    extended_books = db.relationship('ExtendedBook', back_populates='attribute', lazy=True)
