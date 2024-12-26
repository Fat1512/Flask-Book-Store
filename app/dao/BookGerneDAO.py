import pdb

from sqlalchemy import text

import app.dao.BookDAO
from app import db
from app.model.Attribute import Attribute
from app.model.BookGerne import BookGerne
import json


def find_by_id(book_gerne_id):
    return BookGerne.query.get(book_gerne_id)


def find_all_extend_attribute(gerne_id):
    book_gerne = BookGerne.query.get(gerne_id)
    return book_gerne.attributes


def add_gerne(name, parent_id, attributes):
    parent_gerne = BookGerne.query.get(parent_id)

    new_gerne = BookGerne(name=name, lft=parent_gerne.rgt, rgt=parent_gerne.rgt + 1)
    update_left = BookGerne.query.filter(BookGerne.lft >= parent_gerne.rgt).all()
    for item in update_left:
        item.lft += 2

    update_right = BookGerne.query.filter(BookGerne.rgt >= parent_gerne.rgt).all()
    for item in update_right:
        item.rgt += 2

    if attributes:
        for item in attributes:
            attribute = Attribute(attribute_name=item)
            new_gerne.attributes.append(attribute)

    db.session.add(new_gerne)
    db.session.commit()


def remove_gerne(gerne_id):
    gerne = BookGerne.query.get(gerne_id)
    pdb.set_trace()
    step = gerne.rgt - gerne.lft + 1

    update_left = BookGerne.query.filter(BookGerne.lft >= gerne.rgt).all()
    for item in update_left:
        item.lft -= step

    update_right = BookGerne.query.filter(BookGerne.rgt >= gerne.rgt).all()
    for item in update_right:
        item.rgt -= step

    books = app.dao.BookDAO.find_by_gerne(gerne_id)

    for b in books:
        b.book_gerne = BookGerne.query.get(1)

    db.session.delete(gerne)
    db.session.commit()


def get_depth_gerne(id):
    query = """
        SELECT node.book_gerne_id,node.name, node.rgt,node.lft,(COUNT(parent.name) - (sub_tree.depth + 1)) AS depth
        FROM book_gerne AS node,
                 book_gerne AS parent,
                 book_gerne AS sub_parent,
                (
                        SELECT node.name, (COUNT(parent.name) - 1) AS depth
                        FROM book_gerne AS node,
                            book_gerne AS parent
                        WHERE node.lft BETWEEN parent.lft AND parent.rgt
                                AND node.book_gerne_id = :id
                        GROUP BY node.name,node.lft
                        ORDER BY node.lft
                )AS sub_tree
        WHERE node.lft BETWEEN parent.lft AND parent.rgt
                AND node.lft BETWEEN sub_parent.lft AND sub_parent.rgt
                AND sub_parent.name = sub_tree.name
        GROUP BY node.name, sub_tree.depth, node.lft, book_gerne_id
        HAVING (COUNT(parent.name) - (sub_tree.depth + 1)) <= 1
        ORDER BY node.lft;
    """
    result = db.session.execute(text(query), {"id": id})
    rows = result.fetchall()
    # return [BookType(book_type_id=row[0],name=row[1],rgt=row[2],lft=row[3],description=[4]) for row in rows]
    current_gerne = [{
        "id": row[0],
        "name": row[1],
        'rgt': row[2],
        'lft': row[3],
        "depth": row[4]
    } for row in rows if row.depth == 0]
    sub_gerne = [{
        "id": row[0],
        "name": row[1],
        'rgt': row[2],
        'lft': row[3],
        "depth": row[4]
    } for row in rows if row.depth == 1]
    return {
        "current_gerne": current_gerne,
        "sub_gerne": sub_gerne
    }
