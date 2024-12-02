from datetime import datetime
from email.policy import default
from re import findall

from flask import Blueprint, request, render_template
from app import app
from app.dao.BookDAO import find_all, paginate_book, find_by_gerne, find_by_id
from app.dao.BookGerneDAO import get_depth_gerne
from app.dao.CartDao import find_by_cart_id
from app.dao.SearchDAO import searchBook

home_bp = Blueprint('search', __name__)


@home_bp.route('/')
def search_main():
    keyword = request.args.get('keyword')
    minPrice = request.args.get('minPrice', type=float, default=None)
    maxPrice = request.args.get('maxPrice', type=float)
    order = request.args.get('order', default=app.config['ORDER'])
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    gerne_id = request.args.get('gerneId', type=int, default=1)
    book_gerne = get_depth_gerne(gerne_id)

    page = request.args.get('page', 1, type=int)
    pagination = searchBook(keyword, minPrice, maxPrice, order, gerne_id, limit, page)

    return render_template("search.html"
                           , current_gerne=book_gerne["current_gerne"]
                           , sub_gerne=book_gerne["sub_gerne"]
                           , keyword=keyword
                           , minPrice=minPrice
                           , maxPrice=maxPrice
                           , order=order
                           , limit=limit
                           , pagination=pagination)


@home_bp.route('/detail')
def get_detail():
    book_id = request.args.get('bookId', type=int)
    book = find_by_id(book_id)
    books = find_by_gerne(book.book_gerne_id)
    detail_book = {
        "Mã sản phẩm": book.book_id,
        "Tác giả": book.author,
        "Trọng lượng (gr)": book.weight,
        "Kích thước bao bì": book.dimension,
        "Số trang": book.num_page,
        "Hình thức": book.format,
    }
    comments = book.comments
    comments = sorted(comments, key=lambda x: x.created_at, reverse=True)

    for ex in book.extended_books:
        detail_book[ex.attribute.attribute_name] = ex.value

    avg_star = [0, 0, 0, 0, 0]
    avg_rating = 0
    if len(comments):
        for comment in comments:
            avg_rating += comment.star_count
            avg_star[comment.star_count - 1] += 1
        avg_rating = avg_rating / len(comments)

    return render_template("book-detail.html", book=book
                           , detail_book=detail_book
                           , books=books
                           , comments=comments
                           , avg_rating=avg_rating
                           , avg_star=avg_star)
