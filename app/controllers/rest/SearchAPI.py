import math
import sys

from flask import request, jsonify, Blueprint
from app import app
from app.dao.BookGerneDAO import find_by_id
from app.dao.SearchDAO import search_book_es
from app.utils.helper import order_type

search_res_bp = Blueprint('search_rest', __name__)


@search_res_bp.route('/')
def search():

    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=0)
    max_price = request.args.get('maxPrice', type=float, default=9999999999)
    order = request.args.get('order', default='_score')
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    page = request.args.get('page', type=int, default=1)
    gerne_id = request.args.get('gerneId', type=int, default=1)
    book_gerne = find_by_id(gerne_id)
    book = search_book_es(keyword=keyword, min_price=min_price, max_price=max_price, order=order_type[order]
                          , limit=limit
                          , page=page - 1
                          ,lft=book_gerne.lft
                          ,rgt = book_gerne.rgt)
    return jsonify({
        'message': 'success',
        'status': 200,
        'total': int(book['total']),
        'current_page': page,
        'pages': math.ceil(book['total'] / limit),
        'data': book['data'],
        'extended_books': book['extended_books']
    })
