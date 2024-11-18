from sqlalchemy import text
from app import db
from app.model.BookGerne import BookGerne

def get_depth_gerne(id):
    query = """
        SELECT node.book_type_id,node.name, node.rgt,node.lft, node.description,(COUNT(parent.name) - (sub_tree.depth + 1)) AS depth
        FROM book_type AS node,
                 book_type AS parent,
                 book_type AS sub_parent,
                (
                        SELECT node.name, (COUNT(parent.name) - 1) AS depth
                        FROM book_type AS node,
                            book_type AS parent
                        WHERE node.lft BETWEEN parent.lft AND parent.rgt
                                AND node.book_type_id = :id
                        GROUP BY node.name,node.lft
                        ORDER BY node.lft
                )AS sub_tree
        WHERE node.lft BETWEEN parent.lft AND parent.rgt
                AND node.lft BETWEEN sub_parent.lft AND sub_parent.rgt
                AND sub_parent.name = sub_tree.name
        GROUP BY node.name, sub_tree.depth, node.lft, book_type_id
        HAVING (COUNT(parent.name) - (sub_tree.depth + 1)) <= 1
        ORDER BY node.lft;
    """
    result = db.session.execute(text(query), {"id": id})
    rows = result.fetchall()
    # return [BookType(book_type_id=row[0],name=row[1],rgt=row[2],lft=row[3],description=[4]) for row in rows]
    return {
        "data": [
            {
                "id": row[0],
                "name": row[1],
                "depth": row[5]
            }
            for row in rows
        ]
    }
