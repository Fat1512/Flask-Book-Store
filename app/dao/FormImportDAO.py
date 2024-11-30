from app.model.FormImport import FormImport


def get_form_import():
    return FormImport.query.all()