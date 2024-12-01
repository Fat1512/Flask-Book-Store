from sqlalchemy import ForeignKey
from app.model.Comment import Comment

from app import db


class CommentProduct(Comment):
    comment_id = db.Column(db.Integer, ForeignKey('comment.comment_id'), primary_key=True)
    star_count = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
    book = db.relationship('Book', backref='comments', lazy=True)

    comment = db.relationship('Comment', backref='comment_product', lazy=True)
