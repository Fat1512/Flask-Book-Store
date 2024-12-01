from app import db


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    rgt = db.Column(db.Integer)
    lft = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', backref='comments')

