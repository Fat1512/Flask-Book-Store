from app.model.FormImport import FormImport
from app.model.FormImportDetail import FormImportDetail
from app import app, db
from datetime import datetime


def get_form_import():
    return FormImport.query.all()


def create_form_import(form_import_items):
    form_import = FormImport(created_at=datetime.utcnow(), employee_id=2)
    db.session.add(form_import)
    db.session.flush()

    for form_import_item in form_import_items:
        book_id = form_import_item['bookId']
        quantity = form_import_item['quantity']
        form_import_detail = FormImportDetail(book_id=book_id, form_import_id=form_import.form_import_id,
                                              quantity=quantity)
        form_import.form_import_detail.append(form_import_detail)

    db.session.commit()
    return form_import.to_dict()
