from app.model.Book import Book


def searchBook(keyword):
    query= Book.query
    if(keyword):
        query = query.filter(Book.title.contains(keyword))
    return query.all()

