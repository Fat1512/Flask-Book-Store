from app.model.Book import Book
from app.model.FormImport import FormImport
from app.model.FormImportDetail import FormImportDetail
from app import app, db
from datetime import datetime
import math
from sqlalchemy import asc, desc


def find_form_import_by_id(form_import_id):
    form_import = FormImport.query.get(form_import_id)
    return form_import.to_dict()


def find_form_imports(**kwargs):
    form_imports = FormImport.query

    page = int(kwargs.get('page', 1))
    form_import_id = kwargs.get('form_import_id')
    start_date = kwargs.get('start_date')
    end_date = kwargs.get('end_date')

    if form_import_id:
        form_imports = form_imports.filter(FormImport.form_import_id == form_import_id)

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        form_imports = form_imports.filter(FormImport.created_at >= start_date)

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        form_imports = form_imports.filter(FormImport.created_at <= end_date)

    form_imports = form_imports.order_by(desc(FormImport.created_at))

    page_size = app.config['IMPORT_PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    total_page = math.ceil(form_imports.count() / page_size)
    form_imports = form_imports.slice(start, end)

    return {
        'form_imports': form_imports.all(),
        'total_page': total_page,
        'current_page': page
    }


def create_form_import(form_import_items, employee_id):
    form_import = FormImport(created_at=datetime.utcnow(), employee_id=employee_id)

    for form_import_item in form_import_items:
        book_id = form_import_item['bookId']
        quantity = form_import_item['quantity']
        form_import_detail = FormImportDetail(book_id=book_id, form_import=form_import, quantity=quantity)

        book = Book.query.get(book_id)
        book.increase_book(quantity)

        form_import.form_import_detail.append(form_import_detail)

    db.session.add(form_import)
    db.session.commit()
    return form_import.to_dict()
