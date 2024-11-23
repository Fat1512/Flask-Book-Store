from app.model.User import UserRole
from flask import render_template, redirect, url_for
from flask_login import current_user
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.admin_login'))
        if current_user.user_role != UserRole.ADMIN:
            return redirect(url_for('account.admin_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@admin_bp.route("/home")
# @login_required
@admin_required
def admin_home():
    return render_template("admin-home.html")


@admin_bp.route("/add-products")
def add_products_process():
    return render_template("employee-add-products.html")


@admin_bp.route("/statistic")
def admin_statistic():
    return render_template("admin-statistic.html")
