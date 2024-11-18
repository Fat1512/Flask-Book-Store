from re import findall

from flask import Blueprint, request, render_template

from app.dao.BookDAO import find_all
from app.dao.BookGerneDAO import get_depth_gerne

home_bp = Blueprint('search', __name__)
@home_bp.route('/')
def index():
    keyword = request.args.get('keyword')
    books = find_all()
    book_type = get_depth_gerne(1)
    return render_template("index.html",books=books,book_type=book_type,keyword=keyword)



