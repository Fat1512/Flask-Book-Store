from app.model.Book import Book


def find_by_id(id):
    return Book.query.get(id)

def find_all():
    return Book.query.all()