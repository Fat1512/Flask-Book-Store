from datetime import datetime
from email.policy import default
from re import findall

from flask import Blueprint, request, render_template
from app import app
from app.dao.BookDAO import find_all, paginate_book, find_by_gerne, find_by_id
from app.dao.BookGerneDAO import get_depth_gerne
from app.dao.CartDao import find_by_cart_id
from app.dao.SearchDAO import search_book, search_book_es
from app.utils.helper import order_type

home_bp = Blueprint('search', __name__)


@home_bp.route('/')
def search_main():
    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float)
    order = request.args.get('order', default='_score')
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    page = request.args.get('page', type=int, default=1)
    gerne_id = request.args.get('gerneId', type=int, default=1)

    book_gerne = get_depth_gerne(gerne_id)
    book = search_book_es(keyword=keyword, min_price=min_price, max_price=max_price, order=order_type[order]
                          , limit=limit
                          , page=page - 1
                          , lft=book_gerne['current_gerne'][0]['lft']
                          , rgt=book_gerne['current_gerne'][0]['rgt'])
    print('test',book["extended_books"])
    return render_template("search.html"
                           , current_gerne=book_gerne["current_gerne"]
                           , sub_gerne=book_gerne["sub_gerne"]
                           , keyword=keyword
                           , minPrice=min_price
                           , maxPrice=max_price
                           , order=order
                           , limit=limit
                           , extended_books=book["extended_books"]
                           , pagination=book)


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
