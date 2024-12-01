from app import db
from app.model.Comment import Comment
from app.model.CommentProduct import CommentProduct


def create_comment(data):
    comment = data['comment']
    book_id = data.get('bookId')
    star_count = data.get('starCount')

    parent_comment = Comment.query.get(1)
    comment_product_db = CommentProduct(book_id=book_id, star_count=star_count, lft=parent_comment.rgt,
                                        rgt=parent_comment.rgt + 1, content=comment, user_id=2)

    parent_comment.rgt = comment_product_db.rgt + 1
    db.session.add(comment_product_db)

    db.session.commit()


def reply_comment(data):
    comment = data['comment']
    parent_id = data['parentId']
    parent_comment = Comment.query.get(parent_id)

    update_comment = Comment.query.filter(Comment.lft > parent_comment.lft).all()
    comment_db = Comment(content=comment, lft=parent_comment.rgt, rgt=parent_comment.rgt + 1, user_id=2)
    parent_comment.rgt += 2

    for item in update_comment:
        item.lgt += 2
        item.rgt += 2

    db.session.add(comment_db)
    db.session.commit()
