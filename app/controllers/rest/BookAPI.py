import json
from datetime import datetime

from flask import Blueprint, request, jsonify

from app import app
from app.dao.FormImportDAO import find_form_imports, create_form_import, find_form_import_by_id
from app.dao.BookDAO import find_by_id, find_by_barcode, create_book, count_book_sell, upload_images
from app.dao.SearchDAO import search_book

book_rest_bp = Blueprint('book_rest', __name__)


@book_rest_bp.route('/test')
def get_books():
    return find_by_id(54).to_dict()


@book_rest_bp.route('/test1')
def upload():
    upload_images()
    return jsonify({
        "ok": "ok"
    })


@book_rest_bp.route('/<book_id>/sold')
def get_sold(book_id):
    return jsonify({
        'message': 'success',
        'status': 200,
        'soldBook': count_book_sell(book_id)
    })


@book_rest_bp.route('/', methods=['POST'])
def create_books():
    title = request.form.get('title')
    book_gerne_id = request.form.get('book_gerne_id')
    author = request.form.get('author')
    price = request.form.get('price')
    num_page = request.form.get('num_page')
    description = request.form.get('description')
    format = request.form.get('format')
    weight = request.form.get('weight')
    dimension = request.form.get('dimension')
    publisher = request.form.get('publisher')
    release_date = request.form.get('release_date')
    barcode = request.form.get('barcode')

    # Handle book_images (file upload)
    book_images = request.files.getlist('book_images[]')

    # Handle extend_attributes (JSON string)
    extend_attributes = json.loads(request.form.get('extend_attributes'))

    data = {
        "title": title,
        "book_gerne_id": int(book_gerne_id),
        "author": author,
        "price": float(price),
        "num_page": int(num_page),
        "description": description,
        "format": int(format) + 1,
        'publisher': int(publisher),
        "release_date": datetime.strptime(release_date, '%d/%m/%Y'),
        "weight": float(weight),
        "dimension": dimension,
        "book_images": book_images,
        "extend_attributes": extend_attributes,
        "barcode": barcode
    }
    create_book(data)

    return jsonify({
        'message': 'success',
        'status': 200
    })


@book_rest_bp.route('/', methods=['GET'])
def book():
    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float)
    order = request.args.get('order', default=None)
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'])
    gerne_id = request.args.get('gerneId', type=int, default=1)
    page = request.args.get('page', 1, type=int)

    data = search_book(keyword=keyword, min_price=min_price, max_price=max_price, order=order, gerne_id=gerne_id,
                       limit=limit, page=page)
    book_dto = []
    for book in data['books']:
        book_dto.append(book.to_dict())
    data['books'] = book_dto

    return jsonify({
        'message': 'success',
        'status': 200,
        'data': data
    })


@book_rest_bp.route('/manage', methods=['GET'])
def get_manage_books():
    keyword = request.args.get('keyword')
    min_price = request.args.get('minPrice', type=float, default=None)
    max_price = request.args.get('maxPrice', type=float)
    order = request.args.get('order')
    limit = request.args.get('limit', type=int, default=app.config['PAGE_SIZE'] + 10)
    quantity_status = request.args.get("quantityStatus", type=int)
    gerne_id = request.args.get('gerneId', type=int)
    page = request.args.get('page', 1, type=int)

    data = search_book(keyword=keyword, min_price=min_price, max_price=max_price, order=order, gerne_id=gerne_id,
                       limit=limit, page=page, quantity_status=quantity_status)
    book_dto = []

    for book in data['books']:
        book_dto.append(book.to_dict_manage())
    data['books'] = book_dto

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': data
    })


@book_rest_bp.route('/<book_id>/manage', methods=['GET'])
def get_manage_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        jsonify({
            'message': 'Not Found',
            'status': 404
        })

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': book.to_dict_manage()
    })


@book_rest_bp.route('/barcode/<barcode>', methods=['GET'])
def get_by_barcode(barcode):
    barcode = find_by_barcode(barcode).to_dict()

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': barcode
    })


# -------------------------------import book-------------------------------
@book_rest_bp.route('/import', methods=['POST'])
def create_import():
    data = request.json
    form_import = create_form_import(data)

    return jsonify({
        'message': 'Successfully Created',
        'status': 200,
        'data': form_import
    })


@book_rest_bp.route('/import/<int:import_id>/detail')
def get_import_form_detail(import_id):
    form_import = find_form_import_by_id(import_id)

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': form_import
    })


@book_rest_bp.route('/import', methods=['GET'])
def get_import_form():
    form_import_id = request.args.get('formImportId', type=str)
    page = request.args.get('page', 1, type=int)
    start_date = request.args.get('startDate', type=str)
    end_date = request.args.get('endDate', type=str)
    form_imports = find_form_imports(form_import_id=form_import_id, page=page, start_date=start_date, end_date=end_date)

    form_imports['form_imports'] = [form_import.to_dict() for form_import in form_imports['form_imports']]

    return jsonify({
        'message': 'Success',
        'status': 200,
        'data': form_imports
    })
