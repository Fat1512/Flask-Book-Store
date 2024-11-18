from re import findall

from flask import Blueprint, request, render_template

from app.dao.BookDAO import find_all, paginate_book
from app.dao.BookGerneDAO import get_depth_gerne

home_bp = Blueprint('search', __name__)


@home_bp.route('/')
def search_main():
    keyword = request.args.get('keyword')
    book_gerne = get_depth_gerne(1)
    page = request.args.get('page', 1, type=int)
    pagination = paginate_book(page)

    return render_template("search.html"
                           , current_gerne=book_gerne["current_gerne"]
                           , sub_gerne=book_gerne["sub_gerne"]
                           , keyword=keyword
                           , pagination=pagination)
