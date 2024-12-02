from flask import Blueprint, request
from app import app
from app.dao.FormImportDAO import get_form_imports, create_form_import
from app.dao.BookDAO import find_by_id, find_by_barcode
from app.dao.CartDao import find_by_user_id
from app.dao.SearchDAO import searchBook

book_rest_bp = Blueprint('book_rest', __name__)


@book_rest_bp.route('/test')
def get_books():
    return find_by_id(54).to_dict()



@book_rest_bp.route('/', methods=['GET'])
def book():
    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float)
    order = request.args.get('order', default=app.config['ORDER'])
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    gerne_id = request.args.get('gerneId', type=int, default=1)
    page = request.args.get('page', 1, type=int)

    data = searchBook(keyword, min_price, max_price, order, gerne_id, limit, page)
    book_dto = []
    for book in data['books']:
        book_dto.append(book.to_dict())
    data['books'] = book_dto

    return data

@book_rest_bp.route('/manage', methods=['GET'])
def get_manage_books():
    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float)
    order = request.args.get('order')
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    quantity_status = request.args.get("quantityStatus", type=int)
    gerne_id = request.args.get('gerneId', type=int)
    page = request.args.get('page', 1, type=int)

    data = searchBook(keyword, min_price, max_price, order, gerne_id, limit, page, quantity_status)
    book_dto = []

    for book in data['books']:
        book_dto.append(book.to_dict_manage())
    data['books'] = book_dto

    return data


@book_rest_bp.route('/<book_id>/manage', methods=['GET'])
def get_manage_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        return {}
    return book.to_dict_manage()

@book_rest_bp.route('/barcode/<barcode>', methods=['GET'])
def get_by_barcode(barcode):
    barcode = find_by_barcode(barcode).first().to_dict()
    if not barcode:
        return False
    return barcode


@book_rest_bp.route('/test/import', methods=['GET'])
def test_import():
    return [formImport.to_dict() for formImport in get_form_imports()]


@book_rest_bp.route('/import', methods=['POST'])
def create_import():
    data = request.json
    return create_form_import(data)