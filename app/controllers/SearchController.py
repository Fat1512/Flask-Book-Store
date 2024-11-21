from email.policy import default
from re import findall

from flask import Blueprint, request, render_template
from app import app
from app.dao.BookDAO import find_all, paginate_book
from app.dao.BookGerneDAO import get_depth_gerne

home_bp = Blueprint('search', __name__)


@home_bp.route('/')
def search_main():
    keyword = request.args.get('keyword')
    minPrice = request.args.get('minPrice', type=float)
    maxPrice = request.args.get('maxPrice', type=float)
    order = request.args.get('order', default=app.config['ORDER'])
    limit = request.args.get('limit', default=app.config['PAGE_SIZE'])
    gerne_id = request.args.get('gerneId', type=int, default=1)
    book_gerne = get_depth_gerne(gerne_id)
    page = request.args.get('page', 1, type=int)
    pagination = paginate_book(page)

    return render_template("search.html"
                           , current_gerne=book_gerne["current_gerne"]
                           , sub_gerne=book_gerne["sub_gerne"]
                           , keyword=keyword
                           , minPrice=minPrice
                           , maxPrice=maxPrice
                           , order=order
                           , limit=limit
                           , pagination=pagination)
